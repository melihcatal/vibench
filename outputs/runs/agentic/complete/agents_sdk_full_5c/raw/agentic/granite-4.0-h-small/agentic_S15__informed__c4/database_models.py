from typing import Dict, Any

def normalize_item(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw DynamoDB item dict for application use.
    Example: convert DynamoDB attribute values to plain Python types.
    """
    normalized = {}
    for key, value in data.items():
        # Simple mapping; extend as needed
        if isinstance(value, dict) and 'S' in value:
            normalized[key] = value['S']
        elif isinstance(value, dict) and 'N' in value:
            normalized[key] = float(value['N'])
        elif isinstance(value, dict) and 'BOOL' in value:
            normalized[key] = value['BOOL']
        else:
            normalized[key] = value
    return normalized

def upsert_item_payload(identifier: str, data: dict) -> dict:
    """Create UpdateItem payload for upserting a document.
    Uses Set actions for all fields; assumes identifier is the partition key.
    """
    from boto3.dynamodb.conditions import Attr
    payload = {
        'TableName': os.getenv('DYNAMODB_TABLE_NAME'),
        'Key': {'id': {'S': identifier}},
        'UpdateExpression': 'SET ' + ', '.join(f'#{k} = :v{k}' for k in data.keys()),
        'ExpressionAttributeNames': {f'#{k}': k for k in data.keys()},
        'ExpressionAttributeValues': {f':v{k}': {'S': str(v)} for k, v in data.items()},
        'ReturnValues': 'ALL_NEW'
    }
    return payload

def fetch_item_payload(identifier: str) -> dict:
    """Create GetItem payload for fetching a document by its primary key.
    """
    return {
        'TableName': os.getenv('DYNAMODB_TABLE_NAME'),
        'Key': {'id': {'S': identifier}}
    }

def query_item_payload(partition_key: str, filter_expression: str = None, expression_attribute_values: dict = None) -> dict:
    """Create Query payload using partition key; optional filter expression.
    """
    payload = {
        'TableName': os.getenv('DYNAMODB_TABLE_NAME'),
        'KeyConditionExpression': f'#{pk} = :pk_val',
        'ExpressionAttributeNames': {'#pk': partition_key},
        'ExpressionAttributeValues': {':pk_val': {'S': partition_key}}
    }
    if filter_expression:
        payload['FilterExpression'] = filter_expression
    if expression_attribute_values:
        payload['ExpressionAttributeValues'].update(expression_attribute_values)
    return payload

def conditional_update_payload(identifier: str, update_expression: str, expression_attribute_values: dict) -> dict:
    """Create UpdateItem payload with a condition on version (or any attribute). 
    Assumes a 'version' attribute stored as N.
    """
    payload = {
        'TableName': os.getenv('DYNAMODB_TABLE_NAME'),
        'Key': {'id': {'S': identifier}},
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'ConditionExpression': 'attribute_exists(version)',
        'ReturnValues': 'ALL_NEW'
    }
    return payload
