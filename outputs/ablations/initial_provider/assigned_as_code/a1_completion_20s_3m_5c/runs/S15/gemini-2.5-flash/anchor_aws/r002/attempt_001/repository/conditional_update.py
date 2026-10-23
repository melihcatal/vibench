import os
from decimal import Decimal

from database_client import get_dynamodb_resource


def conditional_update(document_id, updates, condition_field, condition_value, table_name=None, key_field=None):
    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
    key_field = key_field or os.environ.get("DYNAMODB_KEY_FIELD", "id")

    if not table_name:
        raise ValueError("DynamoDB table name not provided.")

    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    update_expression_parts = []
    expression_attribute_values = {}
    for k, v in updates.items():
        update_expression_parts.append(f"{k} = :{k}")
        expression_attribute_values[f":{k}"] = v

    update_expression = "SET " + ", ".join(update_expression_parts)
    condition_expression = f"{condition_field} = :current_value"
    expression_attribute_values[":current_value"] = condition_value

    response = table.update_item(
        Key={key_field: document_id},
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW",
    )
    return response.get("Attributes")
