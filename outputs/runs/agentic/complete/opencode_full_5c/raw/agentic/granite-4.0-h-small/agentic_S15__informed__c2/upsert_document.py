import json


def upsert_document(client, table_name, document, primary_key_field="id"):
    """Upsert a JSON document in DynamoDB by its primary identifier."""
    key = {primary_key_field: document[primary_key_field]}
    # Use put_item to perform upsert (insert or replace)
    response = client.put_item(TableName=table_name, Item=document)
    return response
