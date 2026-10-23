import os
import boto3
from boto3.dynamodb.conditions import Attr

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

ddb = boto3.resource("dynamodb")


def conditional_update(identifier, condition, update_expression):
    """Perform a conditional update on a DynamoDB document.

    `condition` should be a boto3.dynamodb.conditions.Attr comparison, e.g. Attr('version').eq(2).
    `update_expression` is a string following DynamoDB Expression syntax, e.g. 'SET status = :val'.
    Returns the updated item or None if condition not met.
    """
    table = ddb.Table(TABLE_NAME)
    try:
        response = table.update_item(
            Key={"id": identifier},
            ConditionExpression=condition,
            UpdateExpression=update_expression,
            ReturnValues="UPDATED_NEW",
        )
        return response.get("Attributes")
    except ddb.meta.client.exceptions.ConditionalCheckFailedException:
        return None
