from database_client import get_container
from database_models import FetchDocumentRequest


def fetch_document(request: FetchDocumentRequest):
    container = get_container()
    if request.partition_key is None:
        return container.read_item(item=request.document_id, partition_key=request.document_id)
    return container.read_item(item=request.document_id, partition_key=request.partition_key)
