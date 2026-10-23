from database_client import get_table


def fetch_document(document_id: str):
    """
    Fetches a document from DynamoDB by its ID.
    """
    table = get_table()
    response = table.get_item(Key={"document_id": document_id})
    item = response.get("Item")
    return item
