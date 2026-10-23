import boto3


def message_audit_store(message):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("your-table-name")
    table.put_item(Item=message)
