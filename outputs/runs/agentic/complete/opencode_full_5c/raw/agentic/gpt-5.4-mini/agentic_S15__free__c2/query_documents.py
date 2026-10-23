import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

from database_client import database_config, get_table
from database_models import build_document_response


def query_documents(
    field_name, field_value, table_name=None, index_name=None, partition_key=None
):
    table = get_table(table_name)
    if partition_key:
        response = table.query(
            KeyConditionExpression=Key(partition_key).eq(field_value),
            IndexName=index_name,
        )
    else:
        response = table.scan(FilterExpression=Attr(field_name).eq(field_value))
    return build_document_response(
        item=response.get("Items", []),
        count=response.get("Count"),
        next_token=response.get("LastEvaluatedKey"),
    )


def main():
    return query_documents(os.environ["FIELD_NAME"], os.environ["FIELD_VALUE"])
