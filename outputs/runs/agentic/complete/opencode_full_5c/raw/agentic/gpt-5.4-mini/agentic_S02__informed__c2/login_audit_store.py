from boto3 import resource


def login_audit_store(record: dict, table_name: str = "federated-login-audit") -> dict:
    table = resource("dynamodb").Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "table": table_name, "record": record}
