from database_client import get_db_client, get_table_name
from boto3.dynamodb.conditions import Key


def query_documents(partition_key_value: str, partition_key_name: str = "document_id"):
    dynamodb = get_db_client()
    table_name = get_table_name()
    table = dynamodb.Table(table_name)

    response = table.query(
        KeyConditionExpression=Key(partition_key_name).eq(partition_key_value)
    )
    return response.get("Items", [])
