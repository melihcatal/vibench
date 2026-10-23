import json
from database_client import get_cosmos_client

def conditional_update(collection_name, doc_id, version, update_payload):
    """Perform a conditional update on a document identified by doc_id.
    The update only succeeds if the document's _etag matches the supplied version.
    Uses Azure Cosmos DB SDK.
    """
    client = get_cosmos_client()
    container = client.get_container_client(collection_name)
    # Construct the conditional request
    options = {"if_match": version}
    container.replace_item(item=doc_id, body=update_payload, **options)
    print(f"Conditional update applied to document {doc_id} (version {version}).")

if __name__ == "__main__":
    # Example usage
    version = "W/\"00000000-0000-0000-0000-000000000001\""
    updates = {"status": "updated", "note": "Conditional update example"}
    conditional_update("mycontainer", "sample-001", version, updates)
