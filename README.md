# Installing

```shell
# clone the repo
git clone https://github.com/geetu040/pricegram_search.git

# go inside the code
cd pricegram_search

# install the requirements
pip install -r requirements.txt

# setup the package
pip install -e .
```

# Usage

```python
from pricegram_search import SearchEngine

def data_fetcher(ids):
    """
    - ids: product ids that are to be fetched from the database
    - this function loads data from the databased based on these ids and returns python list of dictionaries
    - replace this with your code
    """
    return []

engine = SearchEngine(
    data_fetcher = data_fetcher,
    dump_path = "./utils",    # path to utils
)
engine.search(
    keywords = [    # keywords to look for
        "core i5",
        "16gb RAM",
        "512GB SSD"
    ],
    cluster_size = 50,    # create clusters of this size to sort intra
    k = 200,    # fetch these many products
)
```

# Folder Structure

```
.
├── pricegram_search
│   ├── config.py
│   ├── engine.py
│   ├── __init__.py
│   ├── loader.py
│   ├── tests
│   │   ├── integration_tests
│   │   │   ├── test_engine.py
│   │   │   └── test_loader.py
│   │   ├── test_pricegram_search.py
│   │   └── unit_tests
│   │       ├── test_config.py
│   │       └── test_utils.py
│   └── utils.py
├── README.md
├── requirements.txt
├── setup.py
```

The folder structure for the `pricegram_search` Python package is organized as follows:

- **pricegram_search:** This directory serves as the root folder of the Python package.

    - **config.py:** Contains configuration settings for the search engine.
    - **engine.py:** Contains the main implementation of the search engine.
    - **__init__.py:** This file makes the `pricegram_search` folder a Python package.
    - **loader.py:** Provides functionality for loading data into the search engine.
    - **tests:** Contains all test files for the package.
        - **integration_tests:** Contains integration test files.
            - **test_engine.py:** Integration test for the `engine` module.
            - **test_loader.py:** Integration test for the `loader` module.
        - **test_pricegram_search.py:** Test file for the overall `pricegram_search` package.
        - **unit_tests:** Contains unit test files.
            - **test_config.py:** Unit test for the `config` module.
            - **test_utils.py:** Unit test for the `utils` module.
    - **utils.py:** Contains utility functions used by the search engine.

- **README.md:** A Markdown file containing information about the project, including installation and usage instructions.

- **requirements.txt:** Lists the Python packages required by the project.

- **setup.py:** Contains metadata about the project, such as its name, version, and dependencies, used for packaging and distribution.
