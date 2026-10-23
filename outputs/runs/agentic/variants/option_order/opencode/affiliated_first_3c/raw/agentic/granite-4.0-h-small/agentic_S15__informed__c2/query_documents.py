import os
import boto3

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

ddb = boto3.resource("dynamodb")


def query_documents(partition_key, filter_expression=None):
    """Query DynamoDB documents where the partition key matches a given value.

    filter_expression can be a boto3.dynamodb.conditions.Attr clause, e.g. Attr('status').eq('active').
    Returns a list of matching documents.
    """
    table = ddb.Table(TABLE_NAME)
    kwargs = {
        "KeyConditionExpression": Attr(partition_key).eq(os.getenv(partition_key))
    }
    if filter_expression:
        kwargs["FilterExpression"] = filter_expression
    response = table.query(**kwargs)
    return response.get("Items", [])
