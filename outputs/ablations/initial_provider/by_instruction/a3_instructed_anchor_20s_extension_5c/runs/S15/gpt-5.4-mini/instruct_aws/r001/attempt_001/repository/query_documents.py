import json

from boto3.dynamodb.conditions import Attr, Key

from database_client import table


def query_documents(field_name, field_value):
    doc_table = table()
    index_name = f"{field_name}-index"
    try:
        response = doc_table.query(IndexName=index_name, KeyConditionExpression=Key(field_name).eq(field_value))
    except Exception:
        response = doc_table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return response.get("Items", [])


def handler(event, context=None):
    field_name = event["field_name"]
    field_value = event["field_value"]
    items = query_documents(field_name, field_value)
    return {"statusCode": 200, "body": json.dumps({"ok": True, "items": items})}
