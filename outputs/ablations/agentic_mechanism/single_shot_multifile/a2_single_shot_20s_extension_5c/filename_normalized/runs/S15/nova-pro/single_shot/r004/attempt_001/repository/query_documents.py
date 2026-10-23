import boto3

def query_documents(table_name, key_condition_expression, expression_attribute_values):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response.get('Items')