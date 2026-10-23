import os
import json
from database_client import get_dynamodb_client
from database_models import Document, TABLE_NAME

def conditional_update_document(document_id: str, updates: dict, expected_version: int | None = None) -> dict:
    dynamodb = get_dynamodb_client()

    update_expression_parts = []
    expression_attribute_names = {}
    expression_attribute_values = {}

    for key, value in updates.items():
        update_expression_parts.append(f'#{key} = :{key}_val')
        expression_attribute_names[f'#{key}'] = key
        
        # DynamoDB type handling
        if isinstance(value, str): expression_attribute_values[f':{key}_val'] = {'S': value}
        elif isinstance(value, (int, float)): expression_attribute_values[f':{key}_val'] = {'N': str(value)}
        elif isinstance(value, bool): expression_attribute_values[f':{key}_val'] = {'BOOL': value}
        else: expression_attribute_values[f':{key}_val'] = {'S': json.dumps(value)}

    update_expression = 'SET ' + ', '.join(update_expression_parts)
    
    condition_expression = 'attribute_exists(id)'
    if expected_version is not None:
        condition_expression += ' AND #version = :expected_version'
        expression_attribute_names['#version'] = 'version'
        expression_attribute_values[':expected_version'] = {'N': str(expected_version)}
        # Assuming 'version' field exists and is updated with each change for optimistic locking
        # In a real scenario, you'd likely increment 'version' as part of the update_expression
        # or use a different mechanism.

    response = dynamodb.update_item(
        TableName=TABLE_NAME,
        Key={
            'id': {'S': document_id}
        },
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response
