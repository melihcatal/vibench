
import boto3

def fetch_document_by_id(table_name: str, document_id: str) -> dict | None:
    """
    Fetches a document by its identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        document_id: The ID of the document to fetch.

    Returns:
        A dictionary representing the document if found, otherwise None.
    """
    dynamodb = boto3.resource('dynamodb')
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

