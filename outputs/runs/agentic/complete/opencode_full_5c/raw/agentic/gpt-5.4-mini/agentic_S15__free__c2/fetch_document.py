import os

from database_client import get_table
from database_models import build_document_response


def fetch_document(document_id, table_name=None, key_name="id"):
    table = get_table(table_name)
    response = table.get_item(Key={key_name: document_id})
    return build_document_response(
        item=response.get("Item"), consumed_capacity=response.get("ConsumedCapacity")
    )


def main():
    return fetch_document(os.environ["DOCUMENT_ID"])
