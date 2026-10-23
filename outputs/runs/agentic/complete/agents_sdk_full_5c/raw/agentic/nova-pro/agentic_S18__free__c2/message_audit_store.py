import boto3

dynamodb_client = boto3.client('dynamodb')

def store_message_record(table_name, message):
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={'Message': {'S': message}}
    )
    return response