from boto3.dynamodb.conditions import Key
from database_client import get_table

def query_documents_by_category(category: str):
    """
    Queries for documents in Amazon DynamoDB based on a category.

    This assumes a Global Secondary Index (GSI) named 'CategoryIndex'
    exists with 'category' as its partition key.

    :param category: The category to query for.
    :return: A list of items matching the query.
    """
    table = get_table()
    response = table.query(
        IndexName='CategoryIndex',
        KeyConditionExpression=Key('category').eq(category)
    )
    return response.get('Items', [])
