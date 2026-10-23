import os
from database_client import get_dynamodb_client
from database_models import DocumentKey
import boto3


def conditional_update(
    table_name: str,
    key: DocumentKey,
    update_expression: str,
    expression_attribute_values: dict,
    condition_expression: str = None,
):
    dynamodb = get_dynamodb_client()
    update_params = {
        "TableName": table_name,
        "Key": key.model_dump(by_alias=True),
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "UPDATED_NEW",
    }
    if condition_expression:
        update_params["ConditionExpression"] = condition_expression

    response = dynamodb.update_item(**update_params)
    return response
