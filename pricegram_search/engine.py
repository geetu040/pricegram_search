"""Implementation of Search Engine"""
from __future__ import annotations

import warnings

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .loader import Initializer
from .utils import ProductsMatch

warnings.filterwarnings("ignore")


class Pipeline(Initializer, ProductsMatch):
    def pipe(self, **data):
        pipes = {
            "Vectorizer": self.vectorizer_pipe,
            "Cluster": self.cluster_pipe,
            "Sorter": self.sorter_pipe,
        }

        for pipe_name, pipe in pipes.items():
            data = pipe(**data)

        return data

    def vectorizer_pipe(self, **data):
        # preprocessing the querries
        # queries = self.prepare_queries(
        #     data['query'],
        #     data['filters']
        # )
        # queries = [query.strip().lower() for query in data['keywords']]
        queries = self.get_all_combinations(data["keywords"])

        # encoding textual queries to number vector
        encoded = self.vectorizer.transform(queries).toarray()

        return {
            "queries": queries,
            "encoded": encoded,
            **data,
        }

    def cluster_pipe(self, **data):
        # calculating scores
        similarity_scores = cosine_similarity(
            data["encoded"], self.vectors["vectors"]
        )

        # sorting arguments by score
        idx = np.argsort(-similarity_scores.mean(axis=0))

        # selecting top-k
        idx = idx[: data["k"]]

        # getting product ids by vector index
        ids = [self.vectors["ids"][i] for i in idx]

        return {
            "ids": ids,
            **data,
        }

    def sorter_pipe(self, **data):
        c = data["cluster_size"]

        # fetching the data
        products = self.data_fetcher(data["ids"])

        # cleaning queries
        queries = [self.clean_zero(i) for i in data["queries"]]

        # creating splits based on cluster size
        sorted_products = []
        for i in range(0, len(products), c):
            start_i = i
            end_i = start_i + c

            # creating batch
            products_batch = products[start_i:end_i]

            # sorting batch
            products_batch, score, source = self.sort_products(
                products_batch, queries
            )

            # adding batch
            sorted_products.extend(products_batch)

        return {
            "products": sorted_products,
            **data,
        }


class SearchEngine(Pipeline):

    """Downloading and Loading the Utils and Recommending based on keywords"""

    def __init__(self, data_fetcher, dump_path, skip_init=False, verbose=1):
        """Downloading and Loading the Utils"""

        super().__init__()

        self.dump_path = dump_path
        self.data_fetcher = data_fetcher

        # loading the utilities in memory
        self.init(skip_init, verbose)

    def search(self, keywords, cluster_size: int = 50, k: int = 100):
        """
        Recommends products based on keywords.

        Parameters:
        - keywords (List[str]): A list of keywords for product search.
        - cluster_size (int, optional): Size of clusters used for sorting.
          Defaults to 50.
        - k (int, optional): Number of products to fetch. Defaults to 100.

        Returns:
        - List[Dict[str, Any]]: A list of dictionaries
          representing recommended products.

        Algorithm:
        1. If `cluster_size` is greater than `k`, set `cluster_size` to `k`.
        2. Invoke the internal `pipe` method with provided parameters.
        3. Extract the 'products' key from the results and return it.

        Note:
        - The `pipe` method is responsible for processing the keywords,
          clustering, and sorting products.
        - The returned products are a list of dictionaries
          representing recommended products.
        """

        # Validating the inputs
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert isinstance(keywords[0], str)
        assert isinstance(cluster_size, int)
        assert isinstance(k, int)

        # Implementation

        if cluster_size > k:
            cluster_size = k

        results = self.pipe(
            keywords=keywords,
            cluster_size=cluster_size,
            k=k,
        )

        return results["products"]
