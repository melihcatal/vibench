from boto3 import client


def conditional_update(document_id, update_expression, condition_expression, config=None):
    config = config or {}
    dynamodb = client('dynamodb', region_name=config['region'])
    response = dynamodb.update_item(
        TableName=config['table_name'],
        Key={'id': {'S': document_id}},
        UpdateExpression=update_expression,
        ConditionExpression=condition_expression
    )
    return response
