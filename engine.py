import os
import json
import joblib
import time
import numpy as np
import pandas as pd
import tensorflow_hub as hub
from thefuzz import fuzz, process
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

class Initializer():

    def __init__(self):
        self.encoder = None
        self.vectors = None
        self.scaler = None

    def initialize(self):

        # self.encoder = use
        # self.scaler = scaler
        # self.vectors = {
        #     "vectors": vectors,
        #     "labels": linear_ids,
        # }

        dump_path = self.dump_path

        initializers = {
            "Encoder": {
                "path": os.path.join(dump_path, "encoder"),
                "loader": self.load_encoder
            },
            "Scaler": {
                "path": os.path.join(dump_path, "scaler.pkl"),
                "loader": self.load_scaler
            },
            "Vectors": {
                "path": os.path.join(dump_path, "vectors.json"),
                "loader": self.load_vectors
            },
        }

        for name, obj in initializers.items():
            path = obj['path']
            loader = obj['loader']
            time_i = time.time()

            print(f" ------ Loading {name} ({path}) ------ ")
            loader(path)
            print(f" ------ {name} loaded in {round(time.time() - time_i, 3)}s ------ ")

    def load_encoder(self, encoder_path):
        self.encoder = hub.load(encoder_path)

    def load_scaler(self, scaler_path):
        self.scaler = joblib.load(scaler_path)

    def load_vectors(self, vectors_path):
        with open(vectors_path, 'rb') as f:
            vectors = json.load(f)
            for k, v in vectors.items():
                vectors[k] = np.array(v)
            self.vectors = vectors

class Utils(Initializer):
    def preprocess_query(self, query):
        return query.strip().lower()

    def prepare_queries(self, query, filters):

        queries = []

        q = self.preprocess_query(query)
        if q != "": queries.append(q)

        for k, v in filters.items():
            q = f"{k} {v}"
            q = self.preprocess_query(q)
            if q != "": queries.append(q)

        return queries

    def get_fuzzy_score(self, query, row):

        query = query.lower()
        method = lambda x: fuzz.partial_ratio(query, x.lower())

        best_score = -1

        for k, v in row.items():
            if type(v) == list:
                if len(v) == 0: continue
                for item in v:
                    best_score = max(best_score, method(item))

            elif type(v) == dict:
                if len(v) == 0: continue
                for k2, v2 in v.items():
                    best_score = max(best_score, method(f"{k2} {v2}"))

            elif not pd.isna(v):
                best_score = max(best_score, method(f"{k} {v}"))

        return best_score

    def sort_by_fuzz(self, queries, products):
        scores_mat = []
        for q in queries:
            scores_k = []
            for product in products:
                s = self.get_fuzzy_score(q, product)
                scores_k.append(s)
                # sents = product['sentences']
                # processed = process.extractOne(q, sents, scorer=fuzz.partial_ratio)
                # scores_k.append(processed[-1])
            scores_mat.append(scores_k)
        idx = np.argsort(-np.array(scores_mat).mean(axis=0))
        products = [products[i] for i in idx]
        return products

class Pipeline(Utils):

    def pipe(self, **data):

        pipes = {
            "Encoder": self.encoder_pipe,
            "Cluster": self.cluster_pipe,
            "Sorter": self.sorter_pipe,
        }

        for pipe_name, pipe in pipes.items():
            data = pipe(**data)

        return data

    def encoder_pipe(self, **data):

        # preprocessing the querries
        # queries = self.prepare_queries(
        #     data['query'],
        #     data['filters']
        # )
        queries = [query.strip().lower() for query in data['keywords']]

        # encoding textual queries to number vector
        encoded = self.encoder(queries).numpy()

        return {
            'queries': queries,
            'encoded': encoded,
            'k': data['k'],
        }

    def cluster_pipe(self, **data):

        # calculating scores
        similarity_scores = -euclidean_distances(
            data['encoded'],
            self.vectors['vectors']
        )

        # sorting arguments by score
        linear_idx = np.argsort(
            - similarity_scores.mean(axis=0)
        )
        ids = self.vectors['labels'][linear_idx]

        # removing duplicates
        unique_arr, indices = np.unique(ids, return_index=True)
        sorted_indices = np.sort(indices)
        ids = ids[sorted_indices]

        # selecting top-k
        ids = ids[:data['k']]

        return {
            'queries': data['queries'],
            'ids': ids,
        }

    def sorter_pipe(self, **data):

        # fetching the data
        products = self.data_fetcher(data['ids'])

        # sorting the data using fuzzy logic
        products = self.sort_by_fuzz(data['queries'], products)

        return products

class SearchEngine(Pipeline):
    def __init__(self, data_fetcher, dump_path):
        self.dump_path = dump_path
        self.data_fetcher = data_fetcher

        # loading the utilities in memory
        self.initialize()

    def search(self, keywords, k:int=100):
        return self.pipe(
            keywords = keywords,
            k = k,
        )