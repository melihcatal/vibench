import boto3

dynamodb = boto3.client('dynamodb')

def store_message(table_name, message):
    response = dynamodb.put_item(TableName=table_name, Item=message)
    return response