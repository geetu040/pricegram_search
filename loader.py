import os
import json
import joblib
import re
import gdown
from transformers import BertTokenizerFast

from .config import CONFIG

class Utils():
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

class Downloader(Utils):

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

class Loader(Utils):

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
        self.config = CONFIG

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