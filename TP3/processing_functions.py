from utils import load_nlp_model
import simplemma
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from tqdm import tqdm


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


def match_token_in_index(token, index, url):
    match = 0
    if token in index.keys():
        if isinstance(index[token], list):
            if url in index[token]:
                match += 1
        elif isinstance(index[token], dict):
            if url in index[token].keys():
                match += len(index[token][url])
    return match


def count_matching_tokens_in_index(token_list, index, url):
    count = 0
    token_list_without_stopwords = filter_stopwords(token_list)
    for token in token_list_without_stopwords:
        count += match_token_in_index(token, index, url)
    return count, len(token_list_without_stopwords)


def count_matching_tokens_between_document_and_index(token_list, index, products):
    filtered_documents = {}
    for product in products:
        url = product['url']
        nb_matching_tokens, nb_tokens_in_query = count_matching_tokens_in_index(token_list, index, url)
        if nb_matching_tokens != 0:
            filtered_documents[url] = nb_matching_tokens / nb_tokens_in_query
    return filtered_documents


def compute_description_length(products):
    description_length = {}
    for product in tqdm(products):
        description = product["description"]
        tokenised_description = tokenization(description)
        normalised_description = normalize_list_of_tokens(tokenised_description)
        description_length[product["url"]] = len(normalised_description)
    return description_length