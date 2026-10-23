from boto3.dynamodb.conditions import Key
from database_client import get_db_table

def query_documents_by_user(user_id: str):
    """
    Queries for documents belonging to a specific user_id from AWS DynamoDB.

    This query assumes the table has a Global Secondary Index (GSI) named
    'user_id-index' where 'user_id' is the partition key of the index.

    Provider: AWS DynamoDB
    """
    table = get_db_table()
    response = table.query(
        IndexName='user_id-index',
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response.get('Items', [])
