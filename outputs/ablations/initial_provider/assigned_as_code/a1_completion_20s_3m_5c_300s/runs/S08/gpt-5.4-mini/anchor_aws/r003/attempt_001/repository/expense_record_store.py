import boto3


def expense_record_store(payload, config=None):
    client = boto3.resource("dynamodb", region_name=(config or {}).get("region"))
    table = client.Table((config or {}).get("table_name", "expense-records"))
    record = dict(payload.get("record", {}))
    table.put_item(Item=record)
    return {"stored": True, "record": record}
