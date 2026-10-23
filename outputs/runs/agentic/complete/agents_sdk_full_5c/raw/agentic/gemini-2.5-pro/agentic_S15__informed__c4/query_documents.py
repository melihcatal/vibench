from database_client import get_db_table
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from typing import List, Dict

def query_documents_by_category(table_name: str, category: str) -> List[Dict]:
    """
    Queries for documents in an Amazon DynamoDB table based on a category.
    This assumes 'category' is a queryable index (e.g., the partition key or part of a GSI).

    :param table_name: The name of the DynamoDB table.
    :param category: The category value to query for.
    :return: A list of document items matching the query.
    """
    table = get_db_table(table_name)
    if not table:
        raise ConnectionError("Could not connect to the database.")

    try:
        # This assumes 'category' is the partition key.
        # For a more complex schema, you might use a Global Secondary Index (GSI).
        response = table.query(
            KeyConditionExpression=Key('category').eq(category)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error querying category {category}: {e.response['Error']['Message']}")
        raise
