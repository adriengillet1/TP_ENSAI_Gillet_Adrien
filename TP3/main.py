from utils import load_rearranged_products, load_all_index, save_json_file
from processing_functions import select_best_products
from scoring import scoring


if __name__ == "__main__":

    products = load_rearranged_products()

    list_of_index = load_all_index()

    query = "A candy box with cherry chocolates Chocodelade France"

    scores = scoring(query, list_of_index, products.values())

    best_responses_to_query = select_best_products(scores)

    save_json_file(products, best_responses_to_query, "best_responses.json")
