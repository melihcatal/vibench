import boto3


def store_message_audit(message_id, payload):
    client = boto3.client("dynamodb")
    client.put_item(
        TableName="MessageAudit",
        Item={
            "MessageId": {"S": message_id},
            "Payload": {"S": json.dumps(payload)}
        }
    )