import os
from database_client import get_dynamodb_client
from database_models import DocumentQuery
import boto3


def query_documents(table_name: str, query: DocumentQuery):
    dynamodb = get_dynamodb_client()
    if query.field_name and query.field_value:
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="PK = :pk_val",
            FilterExpression=f"{query.field_name} = :field_val",
            ExpressionAttributeValues={
                ":pk_val": {"S": query.partition_key},
                ":field_val": {"S": query.field_value},
            },
        )
    else:
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="PK = :pk_val",
            ExpressionAttributeValues={":pk_val": {"S": query.partition_key}},
        )
    return response.get("Items")
