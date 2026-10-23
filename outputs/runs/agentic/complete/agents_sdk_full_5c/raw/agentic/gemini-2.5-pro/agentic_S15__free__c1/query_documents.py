import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from database_client import get_dynamodb_table

def query_documents_by_category(category: str):
    """
    Queries documents from Amazon DynamoDB based on a category.
    This assumes a Global Secondary Index (GSI) named 'CategoryIndex'
    with 'category' as the partition key.

    Args:
        category: The category to query for.

    Returns:
        A list of documents matching the category.
    """
    table = get_dynamodb_table()
    index_name = os.environ.get("DYNAMODB_GSI_NAME", "CategoryIndex")

    try:
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key('category').eq(category)
        )
        return response.get('Items', [])
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Error: GSI '{index_name}' not found on table.")
        else:
            print(f"An error occurred: {e.response['Error']['Message']}")
        return []
