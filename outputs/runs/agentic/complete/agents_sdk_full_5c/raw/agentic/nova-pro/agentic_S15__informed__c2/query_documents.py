import boto3

dynamodb = boto3.client('dynamodb')

def query_documents(table_name, key_condition_expression, expression_attribute_values):
    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response['Items']