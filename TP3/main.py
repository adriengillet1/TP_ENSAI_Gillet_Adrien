from utils import load_rearranged_products, load_all_index, save_json_file
from processing_functions import select_best_products
from scoring import scoring


if __name__ == "__main__":

    products = load_rearranged_products()

    list_of_index = load_all_index()

    query_test_1 = "A candy box with cherry chocolates Chocodelade France"
    scores_test_1 = scoring(query_test_1, list_of_index, products.values())
    best_responses_to_query_test_1 = select_best_products(scores_test_1)
    save_json_file(products, best_responses_to_query_test_1, "best_responses_query_test_1.json")

    query_test_2 = "dutch blue sneakers"
    scores_test_2 = scoring(query_test_2, list_of_index, products.values())
    best_responses_to_query_test_2 = select_best_products(scores_test_2)
    save_json_file(products, best_responses_to_query_test_2, "best_responses_query_test_2.json")

    query_test_3 = "six Energy drinks GameFuel"
    scores_test_3 = scoring(query_test_3, list_of_index, products.values())
    best_responses_to_query_test_3 = select_best_products(scores_test_3)
    save_json_file(products, best_responses_to_query_test_3, "best_responses_query_test_3.json")