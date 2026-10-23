import boto3

def fetch_document(table_name: str, item_id: str) -> dict | None:
    """
    Fetches a document by its identifier from an AWS DynamoDB table.

    Args:
        table_name: The name of the DynamoDB table.
        item_id: The primary key of the item to fetch.

    Returns:
        The fetched document as a dictionary, or None if not found.
    """
    dynamodb = boto3.resource('dynamodb')  # AWS DynamoDB service client
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'id': item_id  # Assuming 'id' is the primary key attribute name
        }
    )

    return response.get('Item')
