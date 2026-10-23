import boto3


def persist_message_record(table_name: str, record: dict):
    client = boto3.resource("dynamodb", region_name="us-east-1")
    table = client.Table(table_name)
    table.put_item(Item={**record, "provider": "aws-dynamodb"})
    return {"provider": "aws-dynamodb", "stored": True, "record_id": record.get("record_id", "")}
