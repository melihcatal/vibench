import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

from database_client import get_dynamodb_resource


def conditional_update(table_name: str, document_id: str, updates: dict, expected_version: int = None, key_field: str = "id"):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for k, v in updates.items():
        update_expression_parts.append(f"#{k} = :{k}")
        expression_attribute_values[f":{k}"] = v
        expression_attribute_names[f"#{k}"] = k

    update_expression = "SET " + ", ".join(update_expression_parts)

    condition_expression = None
    if expected_version is not None:
        condition_expression = Attr("version").eq(expected_version)
        update_expression_parts.append("#version = :new_version")
        expression_attribute_values[":new_version"] = expected_version + 1
        expression_attribute_names["#version"] = "version"
        update_expression = "SET " + ", ".join(update_expression_parts)


    update_kwargs = {
        "Key": {key_field: document_id},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "UPDATED_NEW",
    }
    
    if expression_attribute_names:
        update_kwargs["ExpressionAttributeNames"] = expression_attribute_names

    if condition_expression:
        update_kwargs["ConditionExpression"] = condition_expression

    response = table.update_item(**update_kwargs)
    return response.get("Attributes")
