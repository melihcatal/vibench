import json
from database_client import get_cosmos_client

def fetch_document(collection_name, doc_id):
    """Retrieve a document by its ID from Cosmos DB container.
    Returns the document as a dict.
    """
    client = get_cosmos_client()
    container = client.get_container_client(collection_name)
    # Get the item
    item = container.read_item(item=doc_id, partition_key=doc_id)
    document = item["item"]
    return document

if __name__ == "__main__":
    # Example usage
    doc = fetch_document("mycontainer", "sample-001")
    print("Fetched document:", json.dumps(doc, indent=2))
