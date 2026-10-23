from database_client import get_table, deserialize_item
from database_models import DocumentResponse


def fetch_document(document_id, table_name=None, partition_key="document_id"):
    table = get_table(table_name)
    key = {partition_key: document_id}

    try:
        response = table.get_item(Key=key, ConsistentRead=True)
        item = response.get("Item")
        if item is None:
            return DocumentResponse(document_id=document_id, data={}, found=False)
        deserialized = deserialize_item(item)
        return DocumentResponse.from_dynamodb_item(deserialized, partition_key)
    except Exception:
        return DocumentResponse(document_id=document_id, data={}, found=False)
