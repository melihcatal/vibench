import boto3


def store_login_audit(record):
    table = boto3.resource("dynamodb").Table(
        __import__("os").environ["LOGIN_AUDIT_TABLE"]
    )
    return table.put_item(Item=record)
