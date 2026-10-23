import os
from typing import Dict, Any
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from database_client import get_table
from database_models import UpdateResult

def conditional_update(identifier: str, updates: Dict[str, Any], expected_version: int) -> UpdateResult:
    table = get_table()
    update_expression = 'SET ' + ', '.join([f'#{k} = :{k}' for k in updates.keys()]) + ', version = version + :inc'
    expression_attribute_names = {f'#{k}': k for k in updates.keys()}
    expression_attribute_names['#version'] = 'version'
    expression_attribute_values = {f':{k}': v for k, v in updates.items()}
    expression_attribute_values[':inc'] = 1
    condition_expression = Attr('version').eq(expected_version)
    try:
        table.update_item(
            Key={'id': identifier},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return True
    except ClientError:
        return False
