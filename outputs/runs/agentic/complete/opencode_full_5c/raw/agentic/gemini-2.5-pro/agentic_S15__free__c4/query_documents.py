from boto3.dynamodb.conditions import Key
from database_client import get_db_table


def query_documents(partition_key_value: str):
    table = get_db_table()
    response = table.query(
        IndexName="PartitionKeyIndex",  # Assuming a GSI on partition_key
        KeyConditionExpression=Key("partition_key").eq(partition_key_value),
    )
    return response.get("Items", [])
