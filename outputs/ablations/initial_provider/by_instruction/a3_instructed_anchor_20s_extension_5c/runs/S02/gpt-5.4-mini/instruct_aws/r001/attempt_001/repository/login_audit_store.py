import boto3


def persist_login_audit_record(record: dict, table_name: str, region: str = "us-east-1"):
    client = boto3.client("dynamodb", region_name=region)
    return {"provider": "AWS DynamoDB", "table_name": table_name, "record": record, "client": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "dynamodb"}
