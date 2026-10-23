import boto3

from database_models import normalize_documents


def query_documents(field_value, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr(config["query_field"]).eq(field_value))
    items = response.get("Items", [])
    return normalize_documents(items)