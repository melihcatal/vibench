from database_client import get_dynamodb_client
from typing import Dict, Any
import json

def conditional_update(table_name: str, document_id: str, update_expression: str, expression_attribute_values: Dict[str, Any], condition_expression: str | None = None) -> Dict[str, Any]:
    dynamodb = get_dynamodb_client()

    # Convert Python types to DynamoDB JSON format for expression_attribute_values
    dynamodb_expression_attribute_values = {}
    for k, v in expression_attribute_values.items():
        if isinstance(v, str):
            dynamodb_expression_attribute_values[k] = {'S': v}
        elif isinstance(v, (int, float)):
            dynamodb_expression_attribute_values[k] = {'N': str(v)}
        elif isinstance(v, bool):
            dynamodb_expression_attribute_values[k] = {'BOOL': v}
        # Add other type mappings as needed

    update_params = {
        'TableName': table_name,
        'Key': {'id': {'S': document_id}},
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': dynamodb_expression_attribute_values,
        'ReturnValues': 'ALL_NEW'
    }

    if condition_expression:
        update_params['ConditionExpression'] = condition_expression

    response = dynamodb.update_item(**update_params)
    
    # Deserialize the updated attributes for easier use
    updated_attributes = response.get('Attributes', {})
    deserialized_attributes = {k: list(v.values())[0] for k, v in updated_attributes.items()}
    return deserialized_attributes
