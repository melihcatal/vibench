import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from database_models import TABLE_NAME
from database_client import get_table

def query_documents_by_category(category: str):
    """
    Queries for documents in the Amazon DynamoDB table by category.
    This assumes a Global Secondary Index (GSI) named 'CategoryIndex'
    with 'category' as the partition key.

    :param category: The category to query for.
    :return: A list of documents matching the category.
    """
    table = get_table(TABLE_NAME)
    try:
        response = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(category)
        )
        items = response.get('Items', [])
        print(f"Found {len(items)} documents in category '{category}'.")
        return items
    except ClientError as e:
        # Handle case where index doesn't exist or other errors
        if e.response['Error']['Code'] == 'ValidationException':
             print(f"Query failed. Ensure a GSI named 'CategoryIndex' exists on table '{TABLE_NAME}' with partition key 'category'.")
        else:
            print(f"Error querying documents: {e.response['Error']['Message']}")
        raise
