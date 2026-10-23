import os
from database_client import get_dynamodb_client

def upsert_document(table_name, primary_key, document):
    """Upsert a JSON document into DynamoDB using the primary identifier.

    Args:
        table_name (str): Name of the DynamoDB table.
        primary_key (str): The attribute name of the primary key.
        document (dict): JSON document to upsert.
    """
    client = get_dynamodb_client()
    # Ensure primary key attribute exists in document
    if primary_key not in document:
        document[primary_key] = str(primary_key)  # Using string conversion for demo
    response = client.put_item(TableName=table_name, Item=document)
    return response
