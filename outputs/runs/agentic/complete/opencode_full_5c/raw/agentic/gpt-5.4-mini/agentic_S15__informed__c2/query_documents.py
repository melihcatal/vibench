from database_client import get_collection
from database_models import DocumentQuery


def query_documents(criteria):
    request = DocumentQuery.from_payload(criteria)
    collection = get_collection()
    return list(collection.find({request.field: request.value}))
