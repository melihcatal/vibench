from messaging_client import dynamodb_resource, get_settings


def message_audit_store(record):
    settings = get_settings()
    table = dynamodb_resource().Table(settings["audit_table_name"])
    return table.put_item(Item=record)
