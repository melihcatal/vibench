import boto3
from document_models import build_standard_expense_schema


def expense_record_store(payload, config=None):
    config = config or {}
    dynamodb = boto3.resource("dynamodb", region_name=config.get("region"))
    table = dynamodb.Table(config["table_name"])
    record = build_standard_expense_schema(payload.get("expense", payload))
    table.put_item(Item=record)
    return {"stored": True, "record": record}
