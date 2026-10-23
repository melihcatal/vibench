from database_client import get_db_table


def fetch_document(document_id: str):
    """
    Fetches a document from DynamoDB by its ID.

    :param document_id: The ID of the document to fetch.
    :return: The document item, or None if not found.
    """
    table = get_db_table()
    response = table.get_item(Key={"document_id": document_id})
    return response.get("Item")
