import os
import boto3
from botocore.exceptions import ClientError
from database_client import TABLE_NAME
from database_models import from_dynamo_item
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def conditional_update(
    identifier: str, update_data: dict, expected_version: int
) -> bool:
    if not update_data:
        return True
    set_expressions = ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
    names = {"#version": "version", **{f"#{k}": k for k in update_data.keys()}}
    values = {f":{k}": v for k, v in update_data.items()}
    values[":one"] = 1
    values[":ver"] = expected_version
    try:
        table.update_item(
            Key={"id": identifier},
            UpdateExpression=f"SET {set_expressions}, version = version + :one",
            ConditionExpression="version = :ver",
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
        )
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return False
        raise
