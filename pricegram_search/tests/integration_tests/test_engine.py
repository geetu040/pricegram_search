from __future__ import annotations

from pricegram_search import SearchEngine


def test_search_engine():
    def data_fetcher(ids):
        return []

    engine = SearchEngine(
        data_fetcher=data_fetcher,
        dump_path="./utils",  # path to utils
        verbose=False,
    )

    engine.search(
        keywords=["core i5", "16gb RAM", "512GB SSD"],  # keywords to look for
        cluster_size=50,  # create clusters of this size to sort intra
        k=200,  # fetch these many products
    )
