import boto3


def message_audit_store(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAuditTable",
        Item={
            "message_id": {"S": message["message_id"]},
            "message_body": {"S": message["message_body"]},
        },
    )
    return response
