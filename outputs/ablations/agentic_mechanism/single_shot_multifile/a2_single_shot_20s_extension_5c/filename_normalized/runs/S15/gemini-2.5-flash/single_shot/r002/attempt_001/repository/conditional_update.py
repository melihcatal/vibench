import os
from database_client import get_dynamodb_client, get_table_name

def conditional_update(document_id: str, updates: dict, condition_field: str = None, expected_value: str = None, version_field: str = None, current_version: int = None):
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for key, value in updates.items():
        update_expression_parts.append(f'#{key} = :{key}')
        expression_attribute_values[f':{key}'] = value
        expression_attribute_names[f'#{key}'] = key

    update_expression = 'SET ' + ', '.join(update_expression_parts)

    condition_expression = None
    if condition_field and expected_value is not None:
        condition_expression = f'#{condition_field} = :{condition_field}'
        expression_attribute_values[f':{condition_field}'] = expected_value
        expression_attribute_names[f'#{condition_field}'] = condition_field

    if version_field and current_version is not None:
        if condition_expression:
            condition_expression += f' AND #{version_field} = :{version_field}'
        else:
            condition_expression = f'#{version_field} = :{version_field}'
        expression_attribute_values[f':{version_field}'] = current_version
        expression_attribute_names[f'#{version_field}'] = version_field

        # Increment version number as part of the update
        update_expression += f', #{version_field} = :{version_field}_new'
        expression_attribute_values[f':{version_field}_new'] = current_version + 1
        if f'#{version_field}' not in expression_attribute_names:
            expression_attribute_names[f'#{version_field}'] = version_field

    try:
        request_args = {
            'TableName': table_name,
            'Key': {'id': document_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ExpressionAttributeNames': expression_attribute_names,
            'ReturnValues': 'ALL_NEW'
        }

        if condition_expression:
            request_args['ConditionExpression'] = condition_expression

        response = dynamodb.update_item(**request_args)
        return {"status": "success", "updated_attributes": response.get('Attributes')}
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {"status": "failed_condition", "message": "Conditional check failed. Document state did not match expected values."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
