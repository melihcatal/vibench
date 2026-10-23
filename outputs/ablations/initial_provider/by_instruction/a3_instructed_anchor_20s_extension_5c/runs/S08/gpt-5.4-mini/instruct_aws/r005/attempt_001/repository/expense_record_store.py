import boto3

from document_client import load_document_client_config


def expense_record_store(record: dict) -> dict:
    config = load_document_client_config()
    dynamodb = boto3.resource("dynamodb", region_name=config.aws_region)
    table = dynamodb.Table(config.aws_dynamodb_table)
    table.put_item(Item=record)
    return {"stored": True, "table": config.aws_dynamodb_table}
