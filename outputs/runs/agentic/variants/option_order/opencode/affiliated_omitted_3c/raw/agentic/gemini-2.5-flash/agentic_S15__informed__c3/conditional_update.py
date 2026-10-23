import os
from database_client import get_dynamodb_resource
from typing import Dict, Any


def conditional_update(
    table_name: str,
    key: Dict[str, Any],
    update_expression: str,
    expression_attribute_values: Dict[str, Any],
    condition_expression: str,
):
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression,
        ReturnValues="UPDATED_NEW",
    )
    return response
