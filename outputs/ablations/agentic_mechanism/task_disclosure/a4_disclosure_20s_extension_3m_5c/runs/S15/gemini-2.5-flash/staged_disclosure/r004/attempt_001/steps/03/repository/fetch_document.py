import os
import boto3
from botocore.exceptions import ClientError

def fetch_document_by_id(table_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The ID of the document to fetch.

    Returns:
        The document as a dictionary if found, otherwise None.
    """
    # AWS credentials and region can be configured via environment variables
    # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME)
    # or assumed roles.
    # For this example, we assume they are configured in the environment or
    # the execution environment has an associated IAM role.
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(
            Key={
                'id': document_id  # Assuming 'id' is the primary key
            }
        )
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching document from DynamoDB: {e.response['Error']['Message']}")
        return None

if __name__ == "__main__":
    # Example Usage (replace with your actual table name and document ID)
    # Ensure AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    # are set in your environment or configure boto3 accordingly.
    
    # You would typically get these from environment variables or a configuration system
    # For demonstration purposes, hardcoding here, but it's not recommended for production.
    # os.environ['AWS_REGION_NAME'] = 'your-aws-region'
    # os.environ['AWS_ACCESS_KEY_ID'] = 'your-access-key-id'
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-access-key'

    # Example: Replace with your actual DynamoDB table name
    my_table_name = "YourDynamoDBTableName"
    my_document_id = "document123"

    print(f"Attempting to fetch document '{my_document_id}' from table '{my_table_name}'...")
    document = fetch_document_by_id(my_table_name, my_document_id)

    if document:
        print(f"Document found: {document}")
    else:
        print(f"Document with ID '{my_document_id}' not found in table '{my_table_name}'.")
