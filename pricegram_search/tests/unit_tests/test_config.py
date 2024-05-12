"""Test cases for Pipeline Configuration"""
from __future__ import annotations

import pytest

from pricegram_search.config import CONFIG

# Import the CONFIG data from the module to be tested


@pytest.fixture(scope="module")
def config():
    return CONFIG


def test_config_not_empty(config):
    assert len(config) > 0, "CONFIG list is empty"


def test_config_items_are_dicts(config):
    for item in config:
        assert isinstance(item, dict), "Item in CONFIG is not a dictionary"


def test_config_items_have_required_keys(config):
    for item in config:
        assert "name" in item, "Name key is missing"
        assert "v" in item, "Version key is missing"
        assert "info" in item, "Info key is missing"


def test_config_name_is_string(config):
    for item in config:
        assert isinstance(item["name"], str), "Name is not a string"


def test_config_version_is_integer(config):
    for item in config:
        assert isinstance(item["v"], int), "Version is not an integer"


def test_config_info_is_dict(config):
    for item in config:
        assert isinstance(item["info"], dict), "Info is not a dictionary"


def test_config_info_path_is_string(config):
    for item in config:
        assert isinstance(item["info"]["path"], str), "Info path not string"
