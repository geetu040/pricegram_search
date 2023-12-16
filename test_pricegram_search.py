import unittest
from unittest.mock import MagicMock, patch
from pricegram_search import SearchEngine

class TestSearchEngine(unittest.TestCase):

	def setUp(self):
		# Mock data_fetcher function
		self.mock_data_fetcher = MagicMock(return_value=[])
		self.engine = SearchEngine(data_fetcher=[], dump_path="./utils", skip_init=True)

	def test_search_valid_inputs(self):
		# Test case for valid inputs

		keywords = ["laptop", "16GB RAM", "512GB SSD"]
		cluster_size = 20
		k = 50

		with patch.object(self.engine, 'pipe', return_value={'products': []}):
			result = self.engine.search(keywords, cluster_size, k)

		self.assertEqual(result, [])

	def test_search_cluster_size_greater_than_k(self):
		# Test case where cluster_size is greater than k
		keywords = ["smartphone", "64GB storage"]
		cluster_size = 30
		k = 20

		with patch.object(self.engine, 'pipe', return_value={'products': []}):
			result = self.engine.search(keywords, cluster_size, k)

		self.assertEqual(result, [])

	def test_search_empty_keywords(self):
		# Test case with empty keywords
		keywords = []
		cluster_size = 30
		k = 20

		with self.assertRaises(AssertionError):
			self.engine.search(keywords, cluster_size, k)

	def test_search_invalid_keywords_type(self):
		# Test case with invalid keywords type
		keywords = "laptop"
		cluster_size = 30
		k = 20

		with self.assertRaises(AssertionError):
			self.engine.search(keywords, cluster_size, k)

	def test_search_invalid_cluster_size_type(self):
		# Test case with invalid cluster_size type
		keywords = ["tablet", "8GB RAM"]
		cluster_size = "30"
		k = 20

		with self.assertRaises(AssertionError):
			self.engine.search(keywords, cluster_size, k)

	def test_search_invalid_k_type(self):
		# Test case with invalid k type
		keywords = ["camera", "20MP"]
		cluster_size = 30
		k = "50"

		with self.assertRaises(AssertionError):
			self.engine.search(keywords, cluster_size, k)

if __name__ == '__main__':
    unittest.main()