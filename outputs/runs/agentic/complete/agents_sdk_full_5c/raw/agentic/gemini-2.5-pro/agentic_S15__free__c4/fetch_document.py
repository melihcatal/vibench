from database_client import get_table

def fetch_document(document_id: str):
    """
    Fetches a single document by its ID from Amazon DynamoDB.

    :param document_id: The unique identifier for the document.
    :return: The document item, or None if not found.
    """
    table = get_table()
    response = table.get_item(
        Key={
            'document_id': document_id
        }
    )
    return response.get('Item')
