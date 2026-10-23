import os

from document_client import dynamodb_resource


def store_expense_record(record: dict, table_name: str | None = None) -> dict:
    table = dynamodb_resource().Table(
        table_name or os.getenv("DYNAMODB_TABLE_NAME", "expense_records")
    )
    table.put_item(Item=record)
    return {"stored": True, "table": table.name}
