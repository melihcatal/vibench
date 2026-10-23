import boto3


def message_audit_store(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAudit",
        Item={
            "MessageId": {"S": message["MessageId"]},
            "Body": {"S": message["Body"]},
            "Timestamp": {"S": str(datetime.datetime.now())},
        },
    )
    return response
