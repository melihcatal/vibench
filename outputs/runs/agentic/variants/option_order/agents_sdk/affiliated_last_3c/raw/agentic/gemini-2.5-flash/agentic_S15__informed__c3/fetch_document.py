import boto3
import os
from database_client import get_dynamodb_client

def fetch_document(table_name: str, document_id: str) -> dict:
    """
    Fetches a document by identifier from a managed NoSQL store (DynamoDB).
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'id': {'S': document_id}
            }
        )
        item = response.get('Item')
        if item:
            print(f"Document fetched successfully: {item}")
            # Example of basic deserialization (DynamoDB JSON to Python dict)
            from database_models import deserialize_dynamodb_item
            return deserialize_dynamodb_item(item)
        else:
            print(f"Document with id {document_id} not found.")
            return None
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # table_name = os.getenv("DYNAMODB_TABLE_NAME", "my-documents-table")
    # document = fetch_document(table_name, "doc123")
    # if document:
    #     print(f"Fetched document: {document}")
    pass
