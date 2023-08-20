import re
from api.serializers import ProductSerializer
from restbase.models import Product
from .engine import SearchEngine
import json

def data_fetcher(pks):
    ids = pks
    products = Product.objects.raw(f'SELECT * FROM product WHERE product.id IN {str(tuple(ids))} ORDER BY FIELD(id, {str(tuple(ids))[1:-1]});')
    serializer = ProductSerializer(products, many=True)
    data = serializer.data
    data = [ dict(i) for i in data ]
    return data


engine = SearchEngine(
    data_fetcher = data_fetcher,
    dump_path = "utils",
)