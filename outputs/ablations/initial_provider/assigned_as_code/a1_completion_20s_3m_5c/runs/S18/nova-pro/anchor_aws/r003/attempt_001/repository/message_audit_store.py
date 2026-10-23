import boto3

from messaging_client import get_resource


def store_message_record(message, config=None):
    config = config or {}
    resource = get_resource("dynamodb", config)
    table = resource.Table(config["table_name"])
    table.put_item(Item=message)