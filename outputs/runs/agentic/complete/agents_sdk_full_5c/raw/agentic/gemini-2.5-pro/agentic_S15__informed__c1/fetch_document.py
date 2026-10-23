from database_client import get_dynamodb_table

def fetch_document(document_id: str):
    """
    Fetches a single document from DynamoDB by its primary key.

    Args:
        document_id: The unique identifier for the document.
    
    Returns:
        The document item if found, otherwise None.
    """
    table = get_dynamodb_table()
    response = table.get_item(
        Key={
            'id': document_id
        }
    )
    return response.get('Item')
