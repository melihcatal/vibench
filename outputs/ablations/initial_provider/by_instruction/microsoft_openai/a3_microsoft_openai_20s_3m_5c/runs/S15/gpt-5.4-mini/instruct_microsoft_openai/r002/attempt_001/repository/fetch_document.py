from database_client import read_item
from database_models import DocumentFetchRequest


def fetch_document(document_id, partition_key=None):
    request = DocumentFetchRequest(document_id=document_id, partition_key=partition_key)
    return read_item(request.document_id, request.partition_key)
