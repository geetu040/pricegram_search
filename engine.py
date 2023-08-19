import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

from .loader import Initializer
from .utils import ProductsMatch

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
        queries = self.get_all_combinations(data['keywords'])

        # encoding textual queries to number vector
        encoded = self.vectorizer.transform(queries).toarray()

        return {
            'queries': queries,
            'encoded': encoded,
            **data,
        }

    def cluster_pipe(self, **data):

        # calculating scores
        similarity_scores = cosine_similarity(
            data['encoded'],
            self.vectors['vectors']
        )

        # sorting arguments by score
        idx = np.argsort(
            - similarity_scores.mean(axis=0)
        )

        # selecting top-k
        idx = idx[:data['k']]

        # getting product ids by vector index
        ids = [self.vectors['ids'][i] for i in idx]

        return {
            'ids': ids,
            **data,
        }

    def sorter_pipe(self, **data):

        c = data['cluster_size']

        # fetching the data
        products = self.data_fetcher(data['ids'])

        # cleaning queries
        queries = [self.clean_zero(i) for i in data['queries']]

        # creating splits based on cluster size
        sorted_products = []
        for i in range(0, len(products), c):
            start_i = i
            end_i = start_i + c

            # creating batch
            products_batch = products[start_i:end_i]

            # sorting batch
            products_batch, score, source = self.sort_products(products_batch, queries)

            # adding batch
            sorted_products.extend(products_batch)

        return {
            "products": sorted_products,
            **data,
        }

class SearchEngine(Pipeline):
    def __init__(self, data_fetcher, dump_path):
        super().__init__()

        self.dump_path = dump_path
        self.data_fetcher = data_fetcher

        # loading the utilities in memory
        self.init()

    def search(self, keywords, cluster_size:int=50, k:int=100):
        if cluster_size > k:
            cluster_size = k

        results = self.pipe(
            keywords = keywords,
            cluster_size = cluster_size,
            k = k,
        )

        return results['products']

if __name__ == "__main__":
    print('hi')