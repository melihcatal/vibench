import boto3

from database_models import normalize_document


def fetch_document(id, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    response = table.get_item(Key={config["key_field"]: id})
    item = response.get("Item")
    if item:
        return normalize_document(item)
    return None