import boto3


def message_audit_store(message):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("MessageAudit")
    table.put_item(Item=message)
    return "Message stored"
