import urllib.parse
import json
import spacy
from spacy.lang.en import English
from collections import defaultdict
import string
import simplemma
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')



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


def synonyms_augmentation(synonyms, token_list):
    augmented_tokens = []
    for token in token_list:
        augmented_tokens.append(token)
        if token in synonyms.keys():
            augmented_tokens.extend(synonyms[token])
    return augmented_tokens


def tokenization(text):
    nlp, PUNCT_TABLE = load_nlp_model()
    doc = nlp(text)
    tokens = []
    for token in doc:
        token = token.text.translate(PUNCT_TABLE).lower()
        if token and token not in nlp.Defaults.stop_words:
            tokens.append(token)
    return tokens


def normalize_list_of_tokens(token_list):
    normalized_tokens = []
    for token in token_list:
        word = simplemma.lemmatize(token, 'en')
        normalized_tokens.append(word)
    return normalized_tokens


def normalize_token(text):
    return simplemma.lemmatize(text, 'en')


def normalize_document_index(document_index):
    normalized_index = {}
    for token in document_index.keys():
        normalized_token = normalize_token(token)
        normalized_index[normalized_token] = document_index[token]
    return normalized_index


def match_token_in_index(token, index, url):
    match = False
    if token in index.keys():
        if url in index[token].keys():
            match = True
    return match


def filter_stopwords(tokens):
    filtered_tokens = []
    stop_words = set(stopwords.words('english'))
    lemmatized_stop_words = []
    for word in list(stop_words):
        lemmatized_stop_words.append(simplemma.lemmatize(word, 'en'))
    for token in tokens:
        if token not in lemmatized_stop_words:
            filtered_tokens.append(token)
    return filtered_tokens


def match_all_tokens_in_index(token_list, index, url):
    token_list_without_stopwords = filter_stopwords(token_list)
    for token in token_list_without_stopwords:
        if not match_token_in_index(token, index, url):
            return False
    return True


def find_document_with_tokens_in_index(token_list, index, products):
    filtered_documents = []
    for product in products:
        url = product['url']
        if match_all_tokens_in_index(token_list, index, url):
            filtered_documents.append(url)
    return filtered_documents

 
def find_document(query, list_of_index, products):
    # process la query pour la transformer en liste de token (comme ml'exemple en bas)
    # faire la recherche des listes de token dans chaque index pour matcher pas que un seul type d'index
    documents_found = {}
    for index_name, index in list_of_index.items():
        documents_found[index_name] = find_document_with_tokens_in_index(query, index, products)
    return documents_found



brand_index = read_json_file("brand_index.json")
origin_index = read_json_file("origin_index.json")
origin_synonyms = read_json_file("origin_synonyms.json")
description_index = read_json_file("description_index.json")
title_index = read_json_file("title_index.json")
reviews_index = read_json_file("reviews_index.json")
products = load_rearranged_products()

list_of_index = {
    "brand_index": brand_index,
    "origin_index": origin_index,
    "origin_synonyms": origin_synonyms,
    "description_index": description_index,
    "title_index": title_index,
    "reviews_index": reviews_index
}


normalized_description_index = normalize_document_index(description_index)
normalized_title_index = normalize_document_index(title_index)



query = "A candy box with chocolates"

print(tokenization(query))

processed_query = normalize_list_of_tokens(tokenization(query))
print(processed_query)

print(find_document_with_tokens_in_index(processed_query, normalized_description_index, products))

print(synonyms_augmentation(origin_synonyms, ["usa", "france", "germany", "italy", "Spain"]))








