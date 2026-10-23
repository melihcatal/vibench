# [SAME-SCENARIO] fetch_document.py
from database_client import get_managed_client


def fetch_document(id: str) -> dict | None:
    """Fetch a JSON document by its primary identifier from Managed NoSQL Store.

    Uses concrete provider integration defined in get_managed_client.
    Returns None if document not found.
    """
    service = "MongoDB Atlas"
    client = get_managed_client()
    if service == "MongoDB Atlas":
        # pymongo find_one by _id
        doc = client["db"]["collection"].find_one({"_id": id})
        return doc
    elif service == "Azure Cosmos DB":
        container = client.get_container("db", "container")
        # cosmos does not have direct get_by_id; query is used
        items = list(
            container.query_items(
                f"SELECT * FROM c WHERE c.id = '{id}'", max_item_count=1
            )
        )
        return items[0] if items else None
    elif service == "IBM Cloudant":
        return client.get_document(id).get("_source")
    raise NotImplementedError(f"Fetch not implemented for {service}")
