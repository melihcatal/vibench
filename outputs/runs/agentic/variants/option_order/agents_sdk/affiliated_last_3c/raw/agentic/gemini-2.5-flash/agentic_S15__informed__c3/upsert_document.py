import boto3
import os
from database_client import get_dynamodb_client

def upsert_document(table_name: str, document: dict):
    """
    Upserts a JSON document into DynamoDB by its primary identifier.
    The document must contain a primary key field (e.g., 'id').
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=document
        )
        print(f"Document upserted successfully: {response}")
        return response
    except Exception as e:
        print(f"Error upserting document: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # and a DynamoDB table named 'my-documents-table' with 'id' as primary key.
    # os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_ACCESS_KEY'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_SECRET_KEY'
    # os.environ['AWS_REGION'] = 'us-east-1' # Example region
    
    # Ensure this environment variable is set or passed
    # table_name = os.getenv("DYNAMODB_TABLE_NAME", "my-documents-table")
    # example_document = {
    #     'id': {'S': 'doc123'},
    #     'title': {'S': 'My First Document'},
    #     'content': {'S': 'This is the content of my first document.'},
    #     'version': {'N': '1'}
    # }
    # upsert_document(table_name, example_document)
    pass
