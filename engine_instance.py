import re
from api.serializers import ProductSerializer
from restbase.models import Product
from .engine import SearchEngine
import json

def data_fetcher(pks):
    ids = pks
    products = []
    products = Product.objects.filter(id__in=ids)
    # for _id in ids:
    #     product = Product.objects.get(id=_id)
    #     products.append(product)
    serializer = ProductSerializer(products, many=True)
    data = serializer.data
    data = [ dict(i) for i in data ]
    return data


engine = SearchEngine(
    data_fetcher = data_fetcher,
    dump_path = "utils",
)