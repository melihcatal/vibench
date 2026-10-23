import boto3


def expense_record_store(record: dict, table_name: str) -> dict:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name}
