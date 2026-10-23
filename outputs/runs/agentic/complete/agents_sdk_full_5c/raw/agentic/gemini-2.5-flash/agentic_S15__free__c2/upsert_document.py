import boto3
import os
from database_client import get_dynamodb_client

def upsert_document(table_name: str, item: dict):
    """
    Upserts a JSON document into DynamoDB by its primary identifier.
    """
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        print(f"Document upserted successfully: {response}")
        return response
    except Exception as e:
        print(f"Error upserting document: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials and a DynamoDB table)
    # os.environ['AWS_REGION'] = 'us-east-1' # Example
    # os.environ['DYNAMODB_TABLE_NAME'] = 'MyDocumentsTable' # Example
    # table_name = os.getenv('DYNAMODB_TABLE_NAME')

    # if table_name:
    #     sample_item = {
    #         'id': {'S': 'doc123'},
    #         'title': {'S': 'My First Document'},
    #         'content': {'S': 'This is the content of the document.'},
    #         'version': {'N': '1'}
    #     }
    #     upsert_document(table_name, sample_item)
    # else:
    #     print("DYNAMODB_TABLE_NAME environment variable not set.")
