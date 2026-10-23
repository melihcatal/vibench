from database_client import get_container
from database_models import DocumentFetchRequest


def fetch_document(request: DocumentFetchRequest) -> dict | None:
    container = get_container()
    try:
        return container.read_item(
            item=request.document_id, partition_key=request.document_id
        )
    except Exception:
        return None
