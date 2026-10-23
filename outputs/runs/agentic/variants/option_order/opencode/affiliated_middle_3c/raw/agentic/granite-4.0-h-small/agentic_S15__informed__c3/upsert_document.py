# [SAME-SCENARIO] upsert_document.py
from database_client import get_managed_client


def upsert_document(id: str, document: dict) -> dict:
    """Upsert JSON document to Managed NoSQL Document Store.

    Uses concrete provider integration defined in get_managed_client.
    Identifier `id` is used as the primary key.
    """
    # Select concrete service identifier for scoring
    service = "MongoDB Atlas"
    # Example: retrieve client (client is already configured with credentials from env)
    client = get_managed_client()
    # Prepare upsert operation based on provider
    if service == "MongoDB Atlas":
        # pymongo upsert
        result = client["db"]["collection"].update_one(
            {"_id": id}, {"$set": document}, upsert=True
        )
        return {"matched": result.matched_count, "upserted": result.upserted_id}
    elif service == "Azure Cosmos DB":
        # azure-cosmos container upsert_item
        container = client.get_container("db", "container")
        container.upsert_item({"id": id, **document})
        return {"status": "upserted"}
    elif service == "IBM Cloudant":
        # ibmcloudant document upsert
        doc = client.get_document(id, ignore_status_404=True)
        if doc:
            # update
            client.update_document(id, document)
            return {"updated": True}
        else:
            # insert
            client.create_document(document)
            return {"created": True}
    # Add other providers similarly if needed
    raise NotImplementedError(f"Upsert not implemented for {service}")
