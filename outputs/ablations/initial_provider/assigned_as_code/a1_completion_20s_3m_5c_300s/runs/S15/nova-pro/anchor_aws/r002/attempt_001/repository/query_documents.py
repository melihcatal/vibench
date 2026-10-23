import boto3

from database_models import deserialize_documents


def query_documents(field_value, field_name, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr(field_name).eq(field_value))
    items = response.get("Items", [])
    return deserialize_documents(items)