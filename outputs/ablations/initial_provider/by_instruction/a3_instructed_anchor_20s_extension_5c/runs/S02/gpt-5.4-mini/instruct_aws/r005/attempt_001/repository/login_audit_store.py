import boto3


def persist_login_audit(record: dict, table_name: str) -> dict:
    client = boto3.resource("dynamodb")
    table = client.Table(table_name)
    table.put_item(Item=record)
    return {"provider": "AWS DynamoDB", "stored": True}
