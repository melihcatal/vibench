import json
from typing import List, Dict, Any
from database_client import client
from database_models import QueryOptions, DocumentResponse


def query_documents(
    filter: Dict[str, Any] = None, options: QueryOptions = None
) -> List[DocumentResponse]:
    """
    Queries documents using the provided filter.
    Optional pagination, sorting and limit are supported via `options`.
    Returns a list of normalized DocumentResponse objects.
    """
    coll = client.get_collection()  # concrete provider call (e.g., pymongo.Collection, DynamoDB table, Firestore client)
    query = filter or {}
    cursor = coll.find(query)
    # Apply sorting if given: expects list of field names; prefix `-` means descending
    sort_spec = []
    if options and options.get("sort"):
        for field in options["sort"]:
            direction = 1
            if field.startswith("-"):
                direction = -1
                field = field[1:]
            sort_spec.append((field, direction))
        cursor = cursor.sort(sort_spec)
    # Apply limit
    if options and options.get("limit"):
        cursor = cursor.limit(options["limit"])
    # Fetch documents
    results = []
    for doc in cursor:
        results.append(
            DocumentResponse(
                id=doc.get("id"),
                data=doc.get("data", {}),
                version=doc.get("version", 0),
            )
        )
    return results


# Simple CLI / test harness (can be removed in production)
if __name__ == "__main__":
    # Example: find all docs with tag "demo", sort by title ascending, limit 5
    filt = {"tags": "demo"}
    opts = QueryOptions(sort=["title"], limit=5)
    docs = query_documents(filt, opts)
    print(json.dumps(docs, indent=2))
