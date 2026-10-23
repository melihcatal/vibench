import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')
table = dynamodb.Table('your_table_name')

def query_documents(key_condition_expression, expression_attribute_values):
    response = table.query(
        KeyConditionExpression=key_condition_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    return response.get('Items')