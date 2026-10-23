from boto3.dynamodb.conditions import Attr, Key

from database_client import dynamodb_table


def query_documents(field_name, field_value, partition_key=None):
    table = dynamodb_table()
    if partition_key is not None:
        response = table.query(KeyConditionExpression=Key("partition_key").eq(str(partition_key)))
        items = response.get("Items", [])
        return [item for item in items if item.get(field_name) == field_value]
    response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return response.get("Items", [])


def handler(event, context=None):
    return query_documents(event["field_name"], event["field_value"], event.get("partition_key"))
