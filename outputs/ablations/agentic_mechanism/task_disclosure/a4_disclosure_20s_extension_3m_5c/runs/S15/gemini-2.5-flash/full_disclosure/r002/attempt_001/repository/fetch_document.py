import boto3
import os

def fetch_document(table_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from an Amazon DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary key of the document to fetch.

    Returns:
        The document as a dictionary, or None if not found.
    """
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(
            Key={
                'id': document_id  # Assuming 'id' is the primary key
            }
        )
        return response.get('Item')
    except Exception as e:
        print(f"Error fetching document from DynamoDB: {e}")
        return None
