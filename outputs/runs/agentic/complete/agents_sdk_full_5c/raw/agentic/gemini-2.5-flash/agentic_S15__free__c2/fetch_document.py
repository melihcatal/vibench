import boto3
import os
from database_client import get_dynamodb_client

def fetch_document(table_name: str, key: dict):
    """
    Fetches a document by identifier from a managed NoSQL store (DynamoDB).
    The key should be in DynamoDB format, e.g., {'id': {'S': 'doc123'}}.
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key=key
        )
        item = response.get('Item')
        if item:
            print(f"Document fetched successfully: {item}")
        else:
            print("Document not found.")
        return item
    except Exception as e:
        print(f"Error fetching document: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a DynamoDB table)
    # os.environ['AWS_REGION'] = 'us-east-1' # Example
    # os.environ['DYNAMODB_TABLE_NAME'] = 'MyDocumentsTable' # Example
    # table_name = os.getenv('DYNAMODB_TABLE_NAME')

    # if table_name:
    #     sample_key = {
    #         'id': {'S': 'doc123'}
    #     }
    #     fetch_document(table_name, sample_key)
    # else:
    #     print("DYNAMODB_TABLE_NAME environment variable not set.")
