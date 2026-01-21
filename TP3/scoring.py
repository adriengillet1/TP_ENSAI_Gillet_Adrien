from collections import defaultdict
import math
from typing import Dict, List
from processing_functions import tokenization, normalize_list_of_tokens, normalize_document_index, count_matching_tokens_between_document_and_index, compute_description_length


# NB : implémentation de la classe BM25InvertedIndex à l'aide de l'IA
class BM25InvertedIndex:

    def __init__(
        self,
        index: Dict[str, Dict[int, List]],
        doc_len: Dict[int, int],
        k1: float = 1.2,
        b: float = 0.75
    ):
        self.index = index
        self.doc_len = doc_len
        self.k1 = k1
        self.b = b

        self.N = len(doc_len)
        self.avgdl = sum(doc_len.values()) / self.N
        self.idf = self._compute_idf()

    def _compute_idf(self):
        idf = {}
        for token, postings in self.index.items():
            df = len(postings)
            idf[token] = math.log(1 + (self.N - df + 0.5) / (df + 0.5))
        return idf

    def score(self, query: List[str]) -> Dict[int, float]:
        scores = defaultdict(float)

        for token in query:
            if token not in self.index:
                continue

            idf = self.idf[token]

            for url, liste_apparition_token in self.index[token].items():
                dl = self.doc_len[url]
                nb_apparition_token = len(liste_apparition_token)

                denom = nb_apparition_token + self.k1 * (
                    1 - self.b + self.b * dl / self.avgdl
                )

                scores[url] += idf * (nb_apparition_token * (self.k1 + 1)) / denom

        return scores

    def rank(self, query: List[str], k: int = 10):
        scores = self.score(query)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]



def scoring(query, list_of_index, products):
    print("Original query : ", query)
    tokenised_query = tokenization(query)
    normalized_query = normalize_list_of_tokens(tokenised_query)
    print("Tokenized and normalized query : ", normalized_query)

    normalized_description_index = normalize_document_index(list_of_index["description_index"])
    results_with_description_index = count_matching_tokens_between_document_and_index(normalized_query, normalized_description_index, products)
    
    normalized_title_index = normalize_document_index(list_of_index["title_index"])
    results_with_title_index = count_matching_tokens_between_document_and_index(normalized_query, normalized_title_index, products)

    results_with_origin_index = count_matching_tokens_between_document_and_index(normalized_query, list_of_index["origin_index"], products)

    results_with_brand_index = count_matching_tokens_between_document_and_index(normalized_query, list_of_index["brand_index"], products)

    unique_url_response = []
    for url in results_with_title_index.keys():
        unique_url_response.append(url)
    for url in results_with_description_index.keys():
        unique_url_response.append(url)
    for url in results_with_origin_index.keys():
        unique_url_response.append(url)
    for url in results_with_brand_index.keys():
        unique_url_response.append(url)
    unique_url_response = set(unique_url_response)

    score = defaultdict(int)

    description_length = compute_description_length(products)
    bm25 = BM25InvertedIndex(list_of_index["description_index"], description_length)

    for url in unique_url_response:
        if url in results_with_title_index.keys():
            score[url] += results_with_title_index[url] * 100
        if url in results_with_description_index.keys():
            score[url] += results_with_description_index[url] * 50
        if url in results_with_origin_index.keys():
            score[url] += 20
        if url in results_with_brand_index.keys():
            score[url] += 40
        mean_mark = list_of_index["reviews_index"][url]["mean_mark"]
        if list_of_index["reviews_index"][url]["total_reviews"] != 0:
            score[url] *= mean_mark
    


    print(bm25.rank(normalized_query))


    return(score)