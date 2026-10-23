import boto3

dynamodb_client = boto3.client("dynamodb")


def message_audit_store(message, table_name):
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={
            "MessageId": {"S": message["MessageId"]},
            "Message": {"S": message["Message"]},
        },
    )
    return response
