import boto3
import os

def fetch_document(table_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary key of the document to fetch.

    Returns:
        A dictionary representing the document, or None if not found.
    """
    # AWS credentials and region are typically managed by environment variables
    # or AWS configuration files.
    # For demonstration, we assume they are configured in the environment.
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_REGION', 'us-east-1') # Example region
    )
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(
            Key={
                'id': document_id  # Assuming 'id' is the primary key name
            }
        )
        return response.get('Item')
    except Exception as e:
        print(f"Error fetching document from DynamoDB: {e}")
        return None
