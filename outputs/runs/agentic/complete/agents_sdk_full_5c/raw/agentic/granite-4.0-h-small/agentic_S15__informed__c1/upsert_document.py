import os
from database_client import get_dynamodb_client
from database_models import parse_item

# Use AWS DynamoDB as the managed NoSQL document store

def upsert_document(pk_value: str, document_body: dict) -> None:
    """Upsert (create or replace) a JSON document in DynamoDB.

    pk_value: primary key identifier for the document (e.g., 'doc-id-123')
    document_body: full JSON document to store.
    """
    client = get_dynamodb_client()
    # DynamoDB expects attribute names wrapped with ExpressionAttributeNames and values in ExpressionAttributeValues
    client.put_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Item=parse_item({"id": pk_value, **document_body})
    )

if __name__ == "__main__":
    # Example usage – remove or comment out in production
    upsert_document("test-doc-1", {"title": "Sample", "content": "Hello world"})
