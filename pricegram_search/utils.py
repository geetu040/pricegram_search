import itertools
import numpy as np
import re
from thefuzz import fuzz

class BasicUtils():
	def clean_zero(self, text):
		return re.sub(r'[^0-9a-zA-Z]', '', text.lower())

	def find_matching_parts(self, input_string, substring):
		matched_parts = []
		start = 0
		while start < len(substring):
			found = False
			for end in range(len(substring), start, -1):
				if substring[start:end] in input_string:
					matched_parts.append(substring[start:end])
					start = end
					found = True
					break
			if not found:
				start += 1
			if start >= len(substring):
				break
		return matched_parts
	
	def get_all_combinations(self, input_list):
		all_combinations = []
		for r in range(1, len(input_list) + 1):
			all_combinations.extend(itertools.combinations(input_list, r))
		return [" ".join(i) for i in all_combinations]

class Algorithms(BasicUtils):
	def matching_ratio(self, text, pattern):
		matches = self.find_matching_parts(text, pattern)
		matches = [i for i in matches if len(i) > 1]

		concat_ratio = len("".join(matches)) / len(pattern)
		n_matches = max(len(matches), 1)

		score = concat_ratio / n_matches
		source = f"{pattern} {'-'.join(matches)} {concat_ratio}-{score} {text}"

		return score, source

	def fuzz_ratio(self, text, pattern):
		score = fuzz.partial_ratio(text, pattern)
		source = f"{pattern} {text}"
		return score, source
	
	def algorithm(self, text, pattern):

		algorithm = self.matching_ratio
		# algorithm = self.fuzz_ratio

		return algorithm(text, pattern)
	
class ProductsMatch(Algorithms):
	def part_keyword(self, part, keyword):
		return self.algorithm(part, keyword)

	def part_keywords(self, part, keywords):
		part = self.clean_zero(part)
		scores = []
		sources = []
		for keyword in keywords:
			score, source = self.part_keyword(part, keyword)
			scores.append(score)
			sources.append(source)
		return scores, sources

	def product_keywords(self, product, keywords):
		keywords = [self.clean_zero(i) for i in keywords]
		scores = []
		sources = []
		for k, v in product.items():
			if type(v) == list:
				for v_ in v:
					part = str(v_)
					score, source = self.part_keywords(part, keywords)
					scores.append(score)
					sources.append(source)

			elif type(v) == dict:
				for k_, v_ in v.items():
					part = k_ + str(v_)
					score, source = self.part_keywords(part, keywords)
					scores.append(score)
					sources.append(source)

			else:
				part = k + str(v)
				score, source = self.part_keywords(part, keywords)
				scores.append(score)
				sources.append(source)

		idx = np.argmax(scores, axis=0)

		scores = np.array(scores)[idx]
		sources = np.array(sources)[idx]

		scores = [scores[i, i] for i in range(len(scores))]
		sources = [sources[i, i] for i in range(len(sources))]

		return scores, sources

	# MAIN
	def sort_products(self, products, keywords):
		scores = []
		sources = []
		for product in products:
			score, source = self.product_keywords(product, keywords)

			score = sum(score)
			source = "\n".join(source)

			scores.append(score)
			sources.append(source)

		idx = np.argsort(scores)[::-1]

		scores = [scores[i] for i in idx]
		sources = [sources[i] for i in idx]
		products = [products[i] for i in idx]

		return products, scores, sources