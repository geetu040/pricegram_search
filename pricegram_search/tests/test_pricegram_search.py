from __future__ import annotations

import json
import os
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from pricegram_search import SearchEngine

OUTPUT = False


class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        # Mock data_fetcher function
        self.mock_data_fetcher = MagicMock(return_value=[])
        self.engine = SearchEngine(
            data_fetcher=[], dump_path="./utils", verbose=0, skip_init=True
        )

    def print_test_info(self, test_name, result):
        if OUTPUT:
            print(f"Test: {test_name}")
            print(f"Result: {result}")
            print("=" * 30)

    def test_search_valid_inputs(self):
        # Test case for valid inputs
        keywords = ["laptop", "16GB RAM", "512GB SSD"]
        cluster_size = 20
        k = 50

        with patch.object(self.engine, "pipe", return_value={"products": []}):
            result = self.engine.search(keywords, cluster_size, k)

        self.print_test_info("test_search_valid_inputs", result)
        self.assertEqual(result, [])

    def test_search_cluster_size_greater_than_k(self):
        # Test case where cluster_size is greater than k
        keywords = ["smartphone", "64GB storage"]
        cluster_size = 30
        k = 20

        with patch.object(self.engine, "pipe", return_value={"products": []}):
            result = self.engine.search(keywords, cluster_size, k)

        self.print_test_info("test_search_cluster_size_greater_than_k", result)
        self.assertEqual(result, [])

    def test_search_empty_keywords(self):
        # Test case with empty keywords
        keywords = []
        cluster_size = 30
        k = 20

        with self.assertRaises(AssertionError):
            _ = self.engine.search(keywords, cluster_size, k)

        self.print_test_info("test_search_empty_keywords", "AssertionError")

    def test_search_invalid_keywords_type(self):
        # Test case with invalid keywords type
        keywords = "laptop"
        cluster_size = 30
        k = 20

        with self.assertRaises(AssertionError):
            _ = self.engine.search(keywords, cluster_size, k)

        self.print_test_info(
            "test_search_invalid_keywords_type", "AssertionError"
        )

    def test_search_invalid_cluster_size_type(self):
        # Test case with invalid cluster_size type
        keywords = ["tablet", "8GB RAM"]
        cluster_size = "30"
        k = 20

        with self.assertRaises(AssertionError):
            _ = self.engine.search(keywords, cluster_size, k)

        self.print_test_info(
            "test_search_invalid_cluster_size_type", "AssertionError"
        )

    def test_search_invalid_k_type(self):
        # Test case with invalid k type
        keywords = ["camera", "20MP"]
        cluster_size = 30
        k = "50"

        with self.assertRaises(AssertionError):
            _ = self.engine.search(keywords, cluster_size, k)

        self.print_test_info("test_search_invalid_k_type", "AssertionError")

    def test_utils_loading(self):
        versions_path = os.path.join(self.engine.dump_path, "versions.json")

        # Check if the path exists
        self.assertTrue(os.path.exists(versions_path), "Utils Downloaded")

        with open(versions_path) as f:
            versions = json.load(f)

        # Check if all versions match
        for conf in self.engine.config:
            version_matches = versions.get(conf["name"], None) == conf["v"]
            self.assertTrue(version_matches, "Utils are not latest")


if __name__ == "__main__":
    unittest.main()
