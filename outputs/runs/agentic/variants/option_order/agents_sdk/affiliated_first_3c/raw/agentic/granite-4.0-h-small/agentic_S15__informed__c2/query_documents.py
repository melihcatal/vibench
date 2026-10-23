import json
from database_client import get_cosmos_client

def query_documents(collection_name, query_filter):
    """Query documents in a Cosmos DB container based on a filter.
    query_filter should be a dict like {'age': {'gt': 30}} or {'tags': {'in': ['python', 'js']}}.
    Returns a list of matching documents.
    """
    client = get_cosmos_client()
    container = client.get_container_client(collection_name)
    # Build a simple query using the SQL API
    # For simplicity we construct an ad-hoc SQL query for the given filter
    sql = "SELECT * FROM c WHERE "
    conditions = []
    for key, cond in query_filter.items():
        if "gt" in cond:
            conditions.append(f"c.{key} > {cond['gt']}")
        elif "in" in cond:
            values = cond["in"]
            placeholders = ','.join(['@' + str(i) for i in range(len(values))])
            conditions.append(f"CONTAINS(c.{key}, {placeholders})")
    if conditions:
        sql += " AND ".join(conditions)
    else:
        sql += " 1=1"
    # Execute the query
    result = container.query_items(query=sql, enable_cross_partition_query=True)
    docs = [d["item"] for d in result]
    return docs

if __name__ == "__main__":
    # Example: find all documents with tag "python"
    matches = query_documents("mycontainer", {"tags": {"in": ["python"]}})
    print(f"Found {len(matches)} documents:", json.dumps(matches, indent=2))
