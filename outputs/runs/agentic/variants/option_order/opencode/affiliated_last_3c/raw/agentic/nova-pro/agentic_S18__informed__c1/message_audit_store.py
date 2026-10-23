import boto3


def message_audit_store(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAuditTable",
        Item={
            "MessageId": {"S": message.message_id},
            "MessageBody": {"S": message.message_body},
        },
    )
    return response
