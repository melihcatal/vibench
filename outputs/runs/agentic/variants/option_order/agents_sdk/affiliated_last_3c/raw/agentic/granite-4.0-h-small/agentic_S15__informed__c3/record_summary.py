import os
from database_client import get_client
from database_models import DocumentModel

def record_summary(document_id):
    """Return a concise summary string for a fetched document.
    Uses the Cosmos DB client to retrieve the document and formats key fields.
    """
    client = get_client()
    container = client["my_container"]
    item = container.read_item(item=document_id, partition_key=document_id)
    doc = DocumentModel.from_dict(item)
    # Example summary: field1=value1, field2=value2 ...
    summary = ", ".join([f"{k}={v}" for k, v in doc.data.items()])
    return f"Document {document_id}: {summary}"
