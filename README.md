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
    dump_path = "./utils",	# path to utils
)
engine.search(
	keywords = [	# keywords to look for
		"core i5",
		"16gb RAM",
		"512GB SSD"
	],
	cluster_size = 50,	# create clusters of this size to sort intra
	k = 200,	# fetch these many products
)
```