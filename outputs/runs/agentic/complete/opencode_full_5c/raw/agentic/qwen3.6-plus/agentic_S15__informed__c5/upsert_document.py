import os
from database_client import get_table, serialize_item
from database_models import DocumentRequest, UpsertResult


def upsert_document(
    document_id, document_data, table_name=None, partition_key="document_id"
):
    table = get_table(table_name)
    request = DocumentRequest(
        document_id=document_id,
        data=document_data,
        partition_key=partition_key,
    )
    item = serialize_item(request.to_dynamodb_item())

    current_version = 0
    try:
        existing = table.get_item(Key={partition_key: document_id})
        if "Item" in existing:
            current_version = existing["Item"].get("version", 0)
    except Exception:
        pass

    new_version = current_version + 1
    item["version"] = new_version

    try:
        table.put_item(Item=item)
        return UpsertResult(
            document_id=document_id,
            success=True,
            version=new_version,
        )
    except Exception as exc:
        return UpsertResult(
            document_id=document_id,
            success=False,
            error=str(exc),
        )
