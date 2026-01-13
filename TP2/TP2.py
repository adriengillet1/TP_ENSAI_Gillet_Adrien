import urllib.parse
import json
import spacy
from spacy.lang.en import English
from collections import defaultdict
import string


def read_jsonl_file():
    products = []
    with open("input/products.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            products.append(json.loads(line))
    return products


def extract_information_from_url(products):
    for product in products:
        url = product["url"]
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.split('/')
        if len(path) > 2:
            product_id = path[2]
            product_variant = parsed_url.query.split('=')[-1]
            if product_variant == '':
                product_variant = None
        else:
            product_id = None
            product_variant = None
        
        product["product_id"] = product_id
        product["product_variant"] = product_variant


def load_nlp_model():
    nlp = English()
    nlp.tokenizer = spacy.tokenizer.Tokenizer(
        nlp.vocab,
        token_match=None
    )
    PUNCT_TABLE = str.maketrans("", "", string.punctuation)
    return nlp, PUNCT_TABLE


def creation_inversed_index(products, field):
    double_defaultdict = lambda: defaultdict(list)
    inversed_index = defaultdict(double_defaultdict)
    
    nlp, PUNCT_TABLE = load_nlp_model()

    for product in products:
        doc = nlp(product[field])
        token_position = 0
        for token in doc:
            token = token.text.translate(PUNCT_TABLE).lower()
            if token and token not in nlp.Defaults.stop_words:
                inversed_index[token][product['url']].append(token_position)
                token_position += 1

    return inversed_index


def creation_review_index(products):
    review_index = defaultdict(dict)
    
    for product in products:
        reviews = product["product_reviews"]
        nb_reviews = len(reviews)
        mean_rating = sum(review["rating"] for review in reviews) / len(reviews) if reviews else 0
        last_review = reviews[-1]["rating"] if reviews else 0

        review_index[product["url"]] = {
            "total_reviews": nb_reviews,
            "mean_mark": mean_rating,
            "last_rating": last_review
        }

    return review_index


def creation_inversed_index_features(products):
    inversed_index_brand = defaultdict(list)
    inversed_index_origin = defaultdict(list)

    for product in products:
        features = product["product_features"]

        brand = features.get("brand")
        origin = features.get("made in")

        if brand:
            inversed_index_brand[brand.lower()].append(product['url'])
        if origin:
            inversed_index_origin[origin.lower()].append(product['url'])

    return inversed_index_brand, inversed_index_origin
    

def save_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)





products = read_jsonl_file()
extract_information_from_url(products)

inversed_index_title = creation_inversed_index(products, "title")
inversed_index_description = creation_inversed_index(products, "description")
review_index = creation_review_index(products)
inversed_index_brand, inversed_index_origin = creation_inversed_index_features(products)

save_json_file(inversed_index_title, "my_inversed_index_title.json")
save_json_file(inversed_index_description, "my_inversed_index_description.json")
save_json_file(review_index, "my_review_index.json")
save_json_file(inversed_index_brand, "my_inversed_index_brand.json")
save_json_file(inversed_index_origin, "my_inversed_index_origin.json")