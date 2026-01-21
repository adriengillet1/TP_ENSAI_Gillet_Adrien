import urllib.parse
from collections import defaultdict
from utils import load_nlp_model


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
    inversed_index_design = defaultdict(list)
    inversed_index_color = defaultdict(list)

    nlp, PUNCT_TABLE = load_nlp_model()

    for product in products:
        features = product["product_features"]

        brand = features.get("brand")
        origin = features.get("made in")
        design = features.get("design")
        colors = features.get("colors")

        if brand:
            inversed_index_brand[brand.lower()].append(product['url'])
        if origin:
            inversed_index_origin[origin.lower()].append(product['url'])
        if design:
            tokens = nlp(design)
            for token in tokens:
                token = token.text.translate(PUNCT_TABLE).lower()
                if token and token not in nlp.Defaults.stop_words:
                    inversed_index_design[token].append(product['url'])
        if colors:
            tokens = nlp(colors)
            for token in tokens:
                token = token.text.translate(PUNCT_TABLE).lower()
                if token and token not in nlp.Defaults.stop_words:
                    inversed_index_color[token].append(product['url'])

    return inversed_index_brand, inversed_index_origin, inversed_index_design, inversed_index_color


