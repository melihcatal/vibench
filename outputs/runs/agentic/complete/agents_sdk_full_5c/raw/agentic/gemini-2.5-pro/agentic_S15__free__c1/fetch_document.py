from botocore.exceptions import ClientError
from database_client import get_dynamodb_table

def fetch_document(document_id: str):
    """
    Fetches a document by its ID from Amazon DynamoDB.

    Args:
        document_id: The ID of the document to fetch.

    Returns:
        The document as a dictionary, or None if not found.
    """
    table = get_dynamodb_table()

    try:
        response = table.get_item(
            Key={
                'id': document_id
            }
        )
    except ClientError as e:
        print(f"Error fetching document: {e.response['Error']['Message']}")
        return None

    item = response.get('Item')
    if item:
        return item
    else:
        print(f"Document with ID {document_id} not found.")
        return None
