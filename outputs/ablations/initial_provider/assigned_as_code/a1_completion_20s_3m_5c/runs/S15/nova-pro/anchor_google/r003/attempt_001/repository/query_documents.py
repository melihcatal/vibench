from boto3 import client


def query_documents(field_value, config=None):
    config = config or {}
    dynamodb = client('dynamodb', region_name=config['region'])
    response = dynamodb.query(
        TableName=config['table_name'],
        KeyConditionExpression='field_name = :value',
        ExpressionAttributeValues={':value': {'S': field_value}}
    )
    items = response.get('Items', [])
    return [{'id': item['id']['S'], 'document': item['document']['S']} for item in items]
