from utils import load_rearranged_products, load_all_index
from scoring import scoring


if __name__ == "__main__":

    products = load_rearranged_products()

    list_of_index = load_all_index()

    query = "A candy box with cherry chocolates Chocodelade France"

    scores = scoring(query, list_of_index, products)
