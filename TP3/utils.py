import json
import spacy
from spacy.lang.en import English
import string

def read_json_file(json_file_name):
    filename = "input/" + json_file_name
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def load_nlp_model():
    nlp = English()
    nlp.tokenizer = spacy.tokenizer.Tokenizer(
        nlp.vocab,
        token_match=None
    )
    PUNCT_TABLE = str.maketrans("", "", string.punctuation)
    return nlp, PUNCT_TABLE


def load_rearranged_products():
    products = []
    with open("rearranged_products.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            products.append(json.loads(line))
    return products


def synonyms_augmentation(synonyms, token):
    augmented_tokens = []
    augmented_tokens.append(token)
    if token in synonyms.keys():
        augmented_tokens.extend(synonyms[token])
    return augmented_tokens


def origin_index_augmentation(origin_index, synonyms):
    augmented_origin_index = {}
    for key in origin_index.keys():
        augmented_keys = synonyms_augmentation(synonyms, key)
        for new_key in augmented_keys:
            augmented_origin_index[new_key] = origin_index[key]
    return augmented_origin_index


def load_all_index():  
    brand_index = read_json_file("brand_index.json")
    origin_index = read_json_file("origin_index.json")
    origin_synonyms = read_json_file("origin_synonyms.json")
    description_index = read_json_file("description_index.json")
    title_index = read_json_file("title_index.json")
    reviews_index = read_json_file("reviews_index.json")

    augmented_origin_index = origin_index_augmentation(origin_index, origin_synonyms)

    list_of_index = {
    "brand_index": brand_index,
    "origin_index": augmented_origin_index,
    "description_index": description_index,
    "title_index": title_index,
    "reviews_index": reviews_index
    }
    return list_of_index


