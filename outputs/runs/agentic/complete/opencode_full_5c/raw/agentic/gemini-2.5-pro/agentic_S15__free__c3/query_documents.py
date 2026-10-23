from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from database_client import get_database_client, get_table_name


def query_documents_by_author(author: str):
    """
    Queries documents from DynamoDB by the author field.
    This assumes a secondary index on the 'author' field.
    """
    dynamodb = get_database_client()
    table = dynamodb.Table(get_table_name())

    try:
        response = table.query(
            IndexName="author-index",  # Assuming a GSI named 'author-index'
            KeyConditionExpression=Key("author").eq(author),
        )
        return response.get("Items", [])
    except ClientError as e:
        # Handle cases where the index might not exist
        if e.response["Error"]["Code"] == "ValidationException":
            # Fallback to scan if no index, not recommended for production
            return query_documents_by_author_scan(author)
        print(f"Error querying documents: {e.response['Error']['Message']}")
        return []


def query_documents_by_author_scan(author: str):
    """
    Queries documents by author using a scan operation.
    NOTE: Scan is inefficient and should be avoided in production.
    """
    dynamodb = get_database_client()
    table = dynamodb.Table(get_table_name())

    try:
        response = table.scan(FilterExpression=Key("author").eq(author))
        return response.get("Items", [])
    except ClientError as e:
        print(f"Error scanning documents: {e.response['Error']['Message']}")
        return []
