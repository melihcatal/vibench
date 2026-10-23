from database_client import get_dynamodb_table
from database_models import Document

def upsert_document(document: Document):
    """
    Creates a new document or replaces an existing one in DynamoDB.

    Args:
        document: A dictionary representing the document to upsert.
                  It must contain the primary key.
    
    Returns:
        The response from DynamoDB's put_item operation.
    """
    table = get_dynamodb_table()
    response = table.put_item(
        Item=document
    )
    return response
