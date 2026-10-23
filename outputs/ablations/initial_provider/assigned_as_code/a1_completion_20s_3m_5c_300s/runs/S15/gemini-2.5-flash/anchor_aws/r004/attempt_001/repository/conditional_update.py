import boto3
from boto3.dynamodb.conditions import Attr
from database_client import get_dynamodb_table
from database_models import DocumentConfig, DocumentPayload
from typing import Dict, Any

def conditional_update(document_id: str, updates: Dict[str, Any], condition_field: str, condition_value: Any, config: DocumentConfig) -> bool:
    table = get_dynamodb_table(config)
    update_expression_parts = []
    expression_attribute_values = {}
    for k, v in updates.items():
        update_expression_parts.append(f"{k} = :{k}")
        expression_attribute_values[f':{k}'] = v

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        table.update_item(
            Key={
                config.key_field: document_id
            },
            UpdateExpression=update_expression,
            ConditionExpression=Attr(condition_field).eq(condition_value),
            ExpressionAttributeValues=expression_attribute_values
        )
        return True
    except boto3.client('dynamodb').exceptions.ConditionalCheckFailedException:
        return False
