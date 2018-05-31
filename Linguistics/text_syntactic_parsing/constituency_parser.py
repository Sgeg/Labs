from allennlp.service.predictors.constituency_parser import sanitize
from allennlp.models.archival import load_archive
from allennlp.service.predictors import Predictor


class ConstituencyParser:
    def __init__(self):
        archive = load_archive(
                    "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo-constituency-parser-2018.03.14.tar.gz"
                )
        self.predictor = Predictor.from_archive(archive, 'constituency-parser')

    # Removes word key from all but leaf nodes. For leaf nodes it replaces token string with token index.
    @staticmethod
    def const_tree_dfs(const_tree, new_tree, index):
        new_node = {'attributes': const_tree['attributes'], 'link': const_tree['link'],
                    'nodeType': const_tree['nodeType']}
        if 'children' in const_tree:
            new_node['children'] = []
            for child in const_tree['children']:
                index = ConstituencyParser.const_tree_dfs(child, new_node['children'], index)
        else:
            new_node['word'] = index
            index += 1
        new_tree.append(new_node)
        return index

    @staticmethod
    def format_const_tree(const_tree):
        new_tree = []
        ConstituencyParser.const_tree_dfs(const_tree, new_tree, 0)
        return new_tree[0]

    def __call__(self, sentence):
        # use predictor on sentence
        pred = predict_sent_span(self.predictor, sentence)
        # get constituency tree from prediction
        const_tree = pred['hierplane_tree']['root']
        # reformat tree and return it
        return ConstituencyParser.format_const_tree(const_tree)


# AllenNLP extension to use custom tokenization
def span_to_instance(self, sent_span):
    sentence_text = [token.text for token in sent_span]
    pos_tags = [token.tag_ for token in sent_span]
    return self._dataset_reader.text_to_instance(sentence_text, pos_tags), {}


# AllenNLP extension to use custom tokenization
def predict_sent_span(self, inputs):
    instance, return_dict = span_to_instance(self, inputs)
    outputs = self._model.forward_on_instance(instance)
    return_dict.update(outputs)
    
    # format the NLTK tree as a string on a single line.
    tree = return_dict.pop("trees")
    return_dict["hierplane_tree"] = self._build_hierplane_tree(tree, 0, is_root=True)
    return_dict["trees"] = tree.pformat(margin=1000000)
    return sanitize(return_dict)
