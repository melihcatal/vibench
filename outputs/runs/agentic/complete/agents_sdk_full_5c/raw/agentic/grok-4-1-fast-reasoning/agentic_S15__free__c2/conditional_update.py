from database_client import get_dynamodb_table
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from typing import Dict, Any

def conditional_update(identifier: str, updates: Dict[str, Any], expected_version: int) -> None:
    table = get_dynamodb_table()
    update_expression_parts = [f'#{key} = :val_{key}' for key in updates.keys()]
    update_expression = 'SET ' + ', '.join(update_expression_parts)
    expression_attribute_names = {f'#{key}': key for key in updates.keys()}
    expression_attribute_values = {f':val_{key}': value for key, value in updates.items()}
    expression_attribute_values[':expected_version'] = expected_version

    try:
        table.update_item(
            Key={'id': identifier},
            UpdateExpression=update_expression,
            ConditionExpression=Attr('version').eq(':expected_version'),
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError(f"Document version mismatch. Expected {expected_version}")
        raise