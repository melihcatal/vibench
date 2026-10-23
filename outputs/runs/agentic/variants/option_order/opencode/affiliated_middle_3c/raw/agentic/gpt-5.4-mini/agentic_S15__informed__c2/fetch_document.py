from database_client import get_table
from database_models import DocumentResponse, normalize_identifier


def fetch_document(identifier):
    key = normalize_identifier(identifier)
    result = get_table().get_item(Key={"id": key})
    document = result.get("Item")
    return DocumentResponse(
        ok=document is not None,
        document=document,
        message="fetched" if document else "not_found",
    )
