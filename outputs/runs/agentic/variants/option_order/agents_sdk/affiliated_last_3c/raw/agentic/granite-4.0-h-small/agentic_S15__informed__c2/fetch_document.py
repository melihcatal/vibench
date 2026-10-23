import os
from database_client import get_dynamodb_client

def fetch_document(table_name, primary_key, key_attr):
    """Fetch a document from DynamoDB by its primary identifier.

    Args:
        table_name (str): DynamoDB table name.
        primary_key (str): Identifier value of the document.
        key_attr (str): Attribute name that serves as the primary key.

    Returns:
        dict: Document data if found, else None.
    """
    client = get_dynamodb_client()
    response = client.get_item(TableName=table_name, Key={key_attr: {'S': str(primary_key)}})
    item = response.get('Item')
    return item
