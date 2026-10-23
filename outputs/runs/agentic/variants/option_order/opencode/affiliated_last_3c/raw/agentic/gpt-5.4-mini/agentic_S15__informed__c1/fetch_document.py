from database_client import get_container
from database_models import DocumentResponse


def fetch_document(document_id, partition_key=None):
    container = get_container()
    result = container.read_item(
        item=document_id, partition_key=partition_key or document_id
    )
    return DocumentResponse(ok=True, document=result).to_dict()
