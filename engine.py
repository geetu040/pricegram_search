import os
import json
import joblib
import time
import itertools
import numpy as np
import re
from thefuzz import fuzz
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import gdown
from transformers import BertTokenizerFast

class LoadingUtils():
    def __init__(self, dump_path):
        self.dump_path = dump_path

    def get_path(self, path):
        return os.path.join(self.dump_path, path)

    def drive_download(self, id, path):
        gdown.download(
            f"https://drive.google.com/uc?id={id}",
            path,
            quiet=False
        )

class Downloader(LoadingUtils):

    def bert_tokenizer(self, info):
        path = self.get_path(info['path'])
        tokenizer = BertTokenizerFast.from_pretrained(info['name'])
        tokenizer.save_pretrained(path)

    def vectorizer(self, info):
        self.drive_download(
            path = self.get_path(info['path']),
            id = info['id'],
        )

    def vectors(self, info):
        self.drive_download(
            path = self.get_path(info['path']),
            id = info['id'],
        )

class Loader(LoadingUtils):

    def bert_tokenizer(self, info):
        path = self.get_path(info['path'])
        tokenizer = BertTokenizerFast.from_pretrained(path)
        return lambda text: tokenizer.convert_ids_to_tokens(
            tokenizer.encode(text, add_special_tokens=False)
        )

    def vectorizer(self, info):
        path = self.get_path(info['path'])
        return joblib.load(path)

    def vectors(self, info):
        path = self.get_path(info['path'])
        with open(path, 'rb') as f:
            return json.load(f)

class Initializer():

    def __init__(self):

        self.dump_path = None
        self.config = [
            {
                "name": "bert_tokenizer",
                "v": 0,
                "info": {
                    "name": "bert-base-uncased",
                    "path": "bert_tokenizer",
                }
            },
            {
                "name": "vectorizer",
                "v": 1,
                "info": {
                    "id": "1Nd8B8-D3lAdA57U9JoHjYKp1J73n_TON",
                    "path": "vectorizer.pkl"
                }
            },
            {
                "name": "vectors",
                "v": 1,
                "info": {
                    "id": "1-AVJp2NaTgtZOOFmWE5VdRRr5_9fQUX2",
                    "path": "vectors.json"
                }
            },
        ]

    def post_init(self):
        self.vectorizer.tokenizer = self.bert_tokenizer
        self.vectorizer.preprocessor = lambda x: re.sub(r'[^0-9a-zA-Z ]', '', x)

    def init(self):

        # 0. Initializers
        self.downloader = Downloader(self.dump_path)
        self.loader = Loader(self.dump_path)

        # 1. Creating Dump Folder
        root = self.dump_path
        if not os.path.exists(root):
            os.makedirs(root)

        # 2. Loading versions of previous downloads
        version_file_path = os.path.join(root, "versions.json")
        if os.path.exists(version_file_path):
            with open(version_file_path, 'rb') as f:
                versions = json.load(f)
        else:
            versions = {}

        # 3. Downloading  and Loading Utils
        get_info_headline = lambda x: f" {x} {name} [v:{v}] ".join(["=" * 20] * 2)
        for dump in self.config:
            name, v, info = list(dump.values())

            # DOWNLOADING
            if versions.get(name) != v:
                print(get_info_headline("Downloading"))
                getattr(
                    self.downloader,
                    name
                )(info)

            # LOADING
            print(get_info_headline("Loading"))
            setattr(
                self,
                name,
                getattr(
                    self.loader,
                    name
                )(info)        
            )

            # Saving Version of dump
            versions[name] = v

        # 4. Saving Latest Versions
        with open(version_file_path, 'w') as f:
            json.dump(versions, f)

        # 5. Post Iniit
        self.post_init()

class Utils(Initializer):
    def get_all_combinations(self, input_list):
        all_combinations = []
        for r in range(1, len(input_list) + 1):
            all_combinations.extend(itertools.combinations(input_list, r))
        return [" ".join(i) for i in all_combinations]

    def clean_zero(self, text):
        # lowercases and keep only digits and alphabets
        return re.sub(r'[^0-9a-z]', '', text.lower())

    def sort_products_by_fuzz(self, products, queries):

        # calculating scores for each product vs all queries
        all_scores = []
        for product in products:
            sent = str(product)  # from python dict to str
            sent = self.clean_zero(sent)
            scores = 0
            for q in queries:
                score = fuzz.partial_ratio(sent, q)
                scores += score
            all_scores.append(scores)

        # sorting the products based on scores
        sorted_idx = np.array(all_scores).argsort()[::-1]
        products = [products[i] for i in sorted_idx]
        # products = [(all_scores[i], products[i]) for i in sorted_idx]

        return products

class Pipeline(Utils):

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
            sorted_product_batch = self.sort_products_by_fuzz(products_batch, queries)

            # adding batch
            sorted_products.extend(sorted_product_batch)

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