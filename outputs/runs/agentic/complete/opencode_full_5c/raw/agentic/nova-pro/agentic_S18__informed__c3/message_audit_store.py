import boto3


# Persist processed message records for later lookup
def store_message_audit(message):
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.put_item(
        TableName="MessageAuditTable",
        Item={
            "MessageId": {"S": message["MessageId"]},
            "Message": {"S": message["Message"]},
            "Timestamp": {"S": message["Timestamp"]},
        },
    )
    return response
