import json
from database_client import get_cosmos_client

def upsert_document(collection_name, doc_id, document):
    """Upsert a single JSON document into Cosmos DB container.
    Uses Azure Cosmos DB SDK.
    """
    client = get_cosmos_client()
    container = client.get_container_client(collection_name)
    # upsert overwrites if exists
    container.upsert_item(body=document)
    print(f"Document {doc_id} upserted.")

if __name__ == "__main__":
    # Example payload
    doc = {
        "id": "sample-001",
        "name": "Sample Document",
        "tags": ["test", "demo"]
    }
    upsert_document("mycontainer", doc["id"], doc)
