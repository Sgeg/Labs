# Text syntactic parsing with spaCy and AllenNLP

Combines spaCy and AllanNLP libraries to perform syntactic parsing of
text.
- SpaCy is used for tokenization, lemmatization, POS tagging and
dependency parsing
- AllenNLP is used for constituency parsing

## Installation (python3)
```bash
pip install -r requirenments.txt
python -m spacy download en
```
## Usage
```python
from text_syntactic_parsing.syntactic_parser import SyntacticParser

parser = SyntacticParser()
text = 'Some random text to parse'
parsed_text = parser(text)
print(parsed_text)
```

```
output:
[{'constituency_tree': {'attributes': ['NP'],
   'children': [{'attributes': ['NP'],
     'children': [{'attributes': ['DT'],
       'link': 'DT',
       'nodeType': 'DT',
       'word': 0},
      {'attributes': ['JJ'], 'link': 'JJ', 'nodeType': 'JJ', 'word': 1},
      {'attributes': ['NN'], 'link': 'NN', 'nodeType': 'NN', 'word': 2}],
     'link': 'NP',
     'nodeType': 'NP'},
    {'attributes': ['PP'],
     'children': [{'attributes': ['IN'],
       'link': 'IN',
       'nodeType': 'IN',
       'word': 3},
      {'attributes': ['NP'],
       'children': [{'attributes': ['NN'],
         'link': 'NN',
         'nodeType': 'NN',
         'word': 4}],
       'link': 'NP',
       'nodeType': 'NP'}],
     'link': 'PP',
     'nodeType': 'PP'}],
   'link': 'NP',
   'nodeType': 'NP'},
  'dependency_tree': [('det', 2, 0),
   ('amod', 2, 1),
   ('ROOT', 2, 2),
   ('aux', 4, 3),
   ('relcl', 2, 4)],
  'tokens': [('Some', 'some', 'DET', ' '),
   ('random', 'random', 'ADJ', ' '),
   ('text', 'text', 'NOUN', ' '),
   ('to', 'to', 'ADP', ' '),
   ('parse', 'parse', 'NOUN', '')]}]
```
## Output format
- constituency_tree: Tree with tokens in leafs and syntactic structures
in other nodes. Each leaf node has 'word' key - an index of token that
corresponds to this node.
- dependency_tree: Dependency tree described as list of dependencies.
Every dependency is a tuple (dependency_type, token from index,
 token to index)
- tokens: every token described as a tuple (token string, token lemma,
token POS, trailing whitespace if present)


