import os
from database_client import NoSQLClient
from database_models import Document

def fetch_document(primary_id: str) -> dict:
    """Retrieve a document by its primary identifier from the managed NoSQL store.

    Uses Amazon DynamoDB as the concrete managed NoSQL document store.
    The table name is defined in the environment variable DYNAMODB_TABLE.
    """
    client = NoSQLClient()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}}
    )
    item = response.get('Item')
    if not item:
        return None
    # Convert DynamoDB types to native Python types
    return Document.from_dict(item).to_dict()
