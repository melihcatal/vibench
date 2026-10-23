import boto3


def store_message_record(record):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(TableName="MessageRecords", Item=record)
    return response
