import boto3


def store_message(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAuditStore",
        Item={
            "MessageId": {"S": message["MessageId"]},
            "Message": {"S": message["Message"]},
        },
    )
    return response
