import os
from decimal import Decimal
import json

import boto3
from botocore.exceptions import ClientError

from database_client import get_dynamodb_client
from database_models import Document


def conditional_update(document_id: str, updates: dict, condition_expression: str, table_name: str, key_field: str = "id", region_name: str = None) -> bool:
    dynamodb = get_dynamodb_client(region_name)
    table = dynamodb.Table(table_name)

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for k, v in updates.items():
        # Use a placeholder for the attribute name to avoid issues with reserved words
        # and ensure correct syntax.
        # E.g., #k0 = :v0
        attr_name_placeholder = f"#attr_{k.replace('.', '_')}"
        attr_value_placeholder = f":val_{k.replace('.', '_')}"

        update_expression_parts.append(f"{attr_name_placeholder} = {attr_value_placeholder}")
        expression_attribute_values[attr_value_placeholder] = json.loads(json.dumps(v), parse_float=Decimal)
        expression_attribute_names[attr_name_placeholder] = k

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        response = table.update_item(
            Key={key_field: document_id},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(f"Conditional check failed for document_id {document_id}.")
            return False
        else:
            raise
