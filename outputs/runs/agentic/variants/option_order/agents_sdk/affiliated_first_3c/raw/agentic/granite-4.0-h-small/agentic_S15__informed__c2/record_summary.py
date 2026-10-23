import json
from database_client import get_cosmos_client
from database_models import normalize_document

def summarize_records(collection_name, max_records=5):
    """Retrieve a limited set of documents and return a concise summary."""
    client = get_cosmos_client()
    container = client.get_container_client(collection_name)
    # Use SQL query to limit results
    query = "SELECT TOP ? * FROM c"
    result = container.query_items(query=query, parameters=[{"value": max_records}], enable_cross_partition_query=True)
    docs = [normalize_document(d["item"]) for d in result]
    summary = {
        "total": len(docs),
        "samples": docs
    }
    return summary

if __name__ == "__main__":
    summary = summarize_records("mycontainer")
    print("Summary of records:", json.dumps(summary, indent=2))
