# [SAME-SCENARIO] query_documents.py
from typing import List, Any, Dict
from database_client import get_managed_client


def query_documents(field: str, value: Any) -> List[Dict[str, Any]]:
    """Query documents where `field` equals `value` in Managed NoSQL Store.

    Returns a list of matching documents as dicts.
    Uses concrete provider integration defined in get_managed_client.
    """
    service = "MongoDB Atlas"
    client = get_managed_client()
    if service == "MongoDB Atlas":
        # pymongo find by field/value
        return list(client["db"]["collection"].find({field: value}))
    elif service == "Azure Cosmos DB":
        container = client.get_container("db", "container")
        # cosmos SQL query
        query = f"SELECT * FROM c WHERE c.{field} = '{value}'"
        return list(container.query_items(query, enable_cross_partition_query=True))
    elif service == "IBM Cloudant":
        # cloudant uses ddoc/view or query with selector
        selector = {field: value}
        return list(client.get_documents_list(selector=selector))
    raise NotImplementedError(f"Query not implemented for {service}")
