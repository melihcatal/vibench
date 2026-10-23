import os
from boto3.dynamodb.conditions import Key, Attr
from database_client import get_dynamodb_resource
from database_models import normalize_document_from_db

def query_documents(table_name: str, key_field: str, key_value: str, filter_field: str = None, filter_value: str = None, index_name: str = None, region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    dynamodb = get_dynamodb_resource(region_name=region_name)
    table = dynamodb.Table(table_name)

    query_kwargs = {
        "KeyConditionExpression": Key(key_field).eq(key_value)
    }

    if filter_field and filter_value:
        query_kwargs["FilterExpression"] = Attr(filter_field).eq(filter_value)

    if index_name:
        query_kwargs["IndexName"] = index_name

    response = table.query(**query_kwargs)
    items = [normalize_document_from_db(item) for item in response.get("Items", [])]

    return items
