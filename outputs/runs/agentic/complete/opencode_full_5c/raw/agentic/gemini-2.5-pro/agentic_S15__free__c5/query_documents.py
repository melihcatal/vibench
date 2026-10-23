from database_client import get_db_table
from boto3.dynamodb.conditions import Key


def query_documents(user_id: str):
    table = get_db_table()

    response = table.query(
        IndexName="userId-index", KeyConditionExpression=Key("userId").eq(user_id)
    )

    return response.get("Items", [])
