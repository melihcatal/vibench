from database_client import get_table
from database_models import FetchResponse


def fetch_document(document_id: str) -> FetchResponse:
    """
    Fetches a document from DynamoDB by its ID.

    Args:
        document_id: The ID of the document to fetch.

    Returns:
        A FetchResponse containing the document or an error indicator.
    """
    table = get_table()
    try:
        response = table.get_item(Key={"document_id": document_id})
        item = response.get("Item")
        if item:
            return {"success": True, "document": item}
        else:
            return {"success": False, "document": None}
    except Exception as e:
        print(f"Error fetching document: {e}")
        return {"success": False, "document": None}
