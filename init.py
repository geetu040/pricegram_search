from .engine import SearchEngine
from restbase.models import Product
from api.serializers import ProductSerializer

def data_fetcher(pks):
    ids = pks.tolist()
    products = Product.objects.filter(id__in=ids)
    serializer = ProductSerializer(products, many=True)
    data = serializer.data
    return data

# CREATING INSTANCE
engine = SearchEngine(
    data_fetcher=data_fetcher,
    dump_path="D:/pricegram-backend/api/pricegram_search/utils",
)
