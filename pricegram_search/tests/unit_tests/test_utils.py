from __future__ import annotations

import pytest

from pricegram_search.utils import ProductsMatch


@pytest.fixture
def products_match_instance():
    return ProductsMatch()


def test_clean_zero():
    utils = ProductsMatch()
    assert utils.clean_zero("abc123") == "abc123"
    assert utils.clean_zero("abc!@#123") == "abc123"
    assert utils.clean_zero("") == ""


def test_find_matching_parts():
    utils = ProductsMatch()
    assert utils.find_matching_parts("abcdef", "def") == ["def"]
    assert utils.find_matching_parts("abcdef", "xyz") == []


def test_get_all_combinations():
    utils = ProductsMatch()
    assert utils.get_all_combinations(["a", "b", "c"]) == [
        "a",
        "b",
        "c",
        "a b",
        "a c",
        "b c",
        "a b c",
    ]


def test_matching_ratio():
    algorithms = ProductsMatch()
    score, _ = algorithms.matching_ratio("abcdef", "def")
    assert score == 1.0


def test_fuzz_ratio():
    algorithms = ProductsMatch()
    score, _ = algorithms.fuzz_ratio("abcdef", "def")
    assert score == 100


def test_algorithm():
    algorithms = ProductsMatch()
    score, _ = algorithms.algorithm("abcdef", "def")
    assert score == 1.0


def test_part_keyword():
    products_match = ProductsMatch()
    score, _ = products_match.part_keyword("abcdef", "def")
    assert score == 1.0


def test_part_keywords():
    products_match = ProductsMatch()
    scores, _ = products_match.part_keywords("abcdef", ["def", "xyz"])
    assert scores == [1.0, 0.0]


def test_product_keywords():
    products_match = ProductsMatch()
    scores, _ = products_match.product_keywords(
        {"key1": "value1"}, ["key", "value"]
    )
    assert scores == [1.0, 1.0]


if __name__ == "__main__":
    pytest.main()
