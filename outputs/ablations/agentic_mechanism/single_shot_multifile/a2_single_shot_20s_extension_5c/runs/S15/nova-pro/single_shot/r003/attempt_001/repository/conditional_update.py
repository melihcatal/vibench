import boto3
from database_client import get_dynamodb_client

def conditional_update(document_id, update_expression, expression_attribute_values):
    client = get_dynamodb_client()
    response = client.update_item(
        TableName='Documents',
        Key={'id': {'S': document_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return response['Attributes']