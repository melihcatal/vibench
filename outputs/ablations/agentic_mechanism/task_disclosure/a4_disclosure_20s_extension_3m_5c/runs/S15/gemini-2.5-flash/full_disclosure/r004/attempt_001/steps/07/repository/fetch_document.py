
import boto3
from botocore.exceptions import ClientError

def fetch_document_from_dynamodb(table_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its primary identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary key of the document to fetch.

    Returns:
        A dictionary representing the document if found, otherwise None.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={'id': document_id})  # Assuming 'id' is the primary key
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching document: {e.response['Error']['Message']}")
        return None
