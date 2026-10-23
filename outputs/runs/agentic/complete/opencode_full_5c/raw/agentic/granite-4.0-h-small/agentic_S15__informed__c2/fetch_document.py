import json


def fetch_document(client, table_name, primary_key_value, primary_key_field="id"):
    """Fetch a JSON document in DynamoDB by its primary identifier."""
    key = {primary_key_field: primary_key_value}
    response = client.get_item(TableName=table_name, Key=key)
    item = response.get("Item")
    return item
