import boto3


def store_message(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAudit",
        Item={
            "MessageId": {"S": message["MessageId"]},
            "Body": {"S": message["Body"]},
            "Timestamp": {"S": message["Timestamp"]},
        },
    )
    return response
