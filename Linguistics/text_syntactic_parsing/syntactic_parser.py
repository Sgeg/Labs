import spacy
from .constituency_parser import ConstituencyParser


class SyntacticParser:
    def __init__(self):
        self.nlp = spacy.load('en')
        self.constituency_parser = ConstituencyParser()

    @staticmethod
    def serialize_spacy_sent(sentence):
        ser_sent = {"tokens": [], "dependency_tree": []}
        for token in sentence:
            ser_sent['tokens'].append((str(token), token.lemma_, token.pos_, token.whitespace_))
            ser_sent['dependency_tree'].append((token.dep_, token.head.i, token.i))
        return ser_sent

    def __call__(self, text):
        doc = self.nlp(text)
        ser_sents = []
        for sent in doc.sents:
            ser_sent = SyntacticParser.serialize_spacy_sent(sent)
            ser_sent['constituency_tree'] = self.constituency_parser(sent)
            ser_sents.append(ser_sent)
        return ser_sents
