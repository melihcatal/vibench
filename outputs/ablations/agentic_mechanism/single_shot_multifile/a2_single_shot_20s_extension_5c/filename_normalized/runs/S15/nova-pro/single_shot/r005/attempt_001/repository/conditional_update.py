import os
from database_client import get_dynamodb_client

def conditional_update(item_id, update_expression, expression_attribute_values):
    client = get_dynamodb_client()
    table_name = os.getenv('DYNAMODB_TABLE_NAME')
    response = client.update_item(
        TableName=table_name,
        Key={'id': {'S': item_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response['Attributes'] if 'Attributes' in response else None