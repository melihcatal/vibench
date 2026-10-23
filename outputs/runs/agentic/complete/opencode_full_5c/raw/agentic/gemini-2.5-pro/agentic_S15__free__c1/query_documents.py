from boto3.dynamodb.conditions import Key
from database_client import get_table


def query_documents(author: str):
    """
    Queries documents by author from the DynamoDB table.
    This assumes a secondary index on the 'author' field.
    """
    table = get_table()
    response = table.query(
        IndexName="author-index", KeyConditionExpression=Key("author").eq(author)
    )
    return response.get("Items", [])
