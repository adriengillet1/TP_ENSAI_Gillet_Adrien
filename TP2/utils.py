import json
import spacy
from spacy.lang.en import English
import string


def read_jsonl_file():
    products = []
    with open("input/products.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            products.append(json.loads(line))
    return products

def load_nlp_model():
    nlp = English()
    nlp.tokenizer = spacy.tokenizer.Tokenizer(
        nlp.vocab,
        token_match=None
    )
    PUNCT_TABLE = str.maketrans("", "", string.punctuation)
    return nlp, PUNCT_TABLE

def save_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)