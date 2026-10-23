import boto3


def login_audit_store(table_name: str, record: dict) -> dict:
    table = boto3.resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return {"provider": "aws-dynamodb", "stored": True}
