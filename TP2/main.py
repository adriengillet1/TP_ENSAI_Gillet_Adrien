from utils import read_jsonl_file, save_json_file
from processing_functions import extract_information_from_url, creation_inversed_index, creation_review_index, creation_inversed_index_features


if __name__ == "__main__":
    products = read_jsonl_file()
    extract_information_from_url(products)

    inversed_index_title = creation_inversed_index(products, "title")
    inversed_index_description = creation_inversed_index(products, "description")
    review_index = creation_review_index(products)
    inversed_index_brand, inversed_index_origin, inversed_index_design, inversed_index_color = creation_inversed_index_features(products)

    save_json_file(inversed_index_title, "my_inversed_index_title.json")
    save_json_file(inversed_index_description, "my_inversed_index_description.json")
    save_json_file(review_index, "my_review_index.json")
    save_json_file(inversed_index_brand, "my_inversed_index_brand.json")
    save_json_file(inversed_index_origin, "my_inversed_index_origin.json")
    save_json_file(inversed_index_design, "my_inversed_index_design.json")
    save_json_file(inversed_index_color, "my_inversed_index_color.json")