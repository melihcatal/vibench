import boto3


def expense_record_store(record, table_name):
    client = boto3.resource("dynamodb")
    table = client.Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table_name": table_name}
