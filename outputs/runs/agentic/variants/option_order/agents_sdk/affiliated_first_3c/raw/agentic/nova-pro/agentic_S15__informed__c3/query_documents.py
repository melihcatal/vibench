import boto3

dynamodb = boto3.client('dynamodb')

def query_documents(table_name, key_condition):
    response = dynamodb.query(TableName=table_name, KeyConditionExpression=key_condition)
    return response.get('Items')