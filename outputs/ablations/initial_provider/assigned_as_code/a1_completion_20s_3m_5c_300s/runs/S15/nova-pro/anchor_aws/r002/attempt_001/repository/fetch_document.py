import boto3

from database_models import deserialize_document


def fetch_document(document_id, config):
    table = boto3.resource("dynamodb", region_name=config["region"]).Table(config["table_name"])
    response = table.get_item(Key={config["key_field"]: document_id})
    item = response.get("Item")
    if item:
        return deserialize_document(item)
    return None