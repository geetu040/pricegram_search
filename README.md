# Usage

```python
from pricegram_search import SearchEngine

def data_fetcher(ids):
	"""
	ids: product ids that are to be fetched from the database
	this function loads data from the databased based on these ids replace this with your code
	""" 
	return []

engine = SearchEngine(
    data_fetcher = data_fetcher,
    dump_path = "./pricegram_search/utils",	# path to utils
)
```