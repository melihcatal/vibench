import boto3


def persist_message_record(record: dict, table_name: str) -> dict:
    client = boto3.resource("dynamodb")
    table = client.Table(table_name)
    table.put_item(Item=record)
    return {
        "status": "stored",
        "table": table_name,
        "message_id": record.get("message_id", ""),
    }
