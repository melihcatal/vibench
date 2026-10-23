import os
from database_client import get_dynamodb_client
from database_models import Document

# Managed NoSQL store: Amazon DynamoDB

def fetch_document(doc_id: str) -> Document:
    """Retrieve a document by its primary identifier from DynamoDB.

    Returns a Document object on success or raises a RuntimeError.
    """
    client = get_dynamodb_client()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={"id": {"S": doc_id}}
    )
    item = response.get('Item')
    if not item:
        raise RuntimeError(f"Document {doc_id} not found")
    return Document.from_dynamodb_item(item)

if __name__ == "__main__":
    # Example usage
    try:
        doc = fetch_document('test-doc-1')
        print('Fetched:', doc)
    except Exception as e:
        print('Error:', e)
