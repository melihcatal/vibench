import boto3


def audit_summary(table_name: str) -> dict:
    table = boto3.resource("dynamodb").Table(table_name)
    items = table.scan().get("Items", [])
    return {"provider": "aws-dynamodb", "event_count": len(items)}
