from azure.cosmos import MatchConditions

from database_client import get_container
from database_models import build_response, normalize_document


def upsert_document(document):
    item = normalize_document(document)
    container = get_container()
    result = container.upsert_item(item)
    return build_response(result)
