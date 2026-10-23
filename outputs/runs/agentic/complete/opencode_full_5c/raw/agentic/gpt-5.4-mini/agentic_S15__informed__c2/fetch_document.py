from database_client import get_collection
from database_models import DocumentIdentifier


def fetch_document(identifier):
    request = DocumentIdentifier.from_payload(identifier)
    collection = get_collection()
    return collection.find_one({request.id_field: request.value})
