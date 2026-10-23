# [SAME-SCENARIO] conditional_update.py
from database_client import get_managed_client


def conditional_update(id: str, version: int, update_fields: dict) -> bool:
    """Apply a version-aware (conditional) update to a document in Managed NoSQL Store.

    Only performs update if current version of the document matches `version`. Returns True if update succeeded.
    Uses concrete provider integration defined in get_managed_client.
    """
    service = "MongoDB Atlas"
    client = get_managed_client()
    if service == "MongoDB Atlas":
        result = client["db"]["collection"].update_one(
            {"_id": id, "version": version},
            {"$set": update_fields, "$inc": {"version": 1}},
        )
        return result.matched_count > 0
    elif service == "Azure Cosmos DB":
        # Cosmos does not support native conditional update via SDK; we can use upsert with conditional
        container = client.get_container("db", "container")
        # Draft: attempt update with conditional via replace_item
        try:
            item = container.read_item(id)
            # check version locally
            if item.get("version") == version:
                updated = {**item, **update_fields, "version": version + 1}
                container.replace_item(item["id"], updated)
                return True
        except Exception:
            pass
        return False
    elif service == "IBM Cloudant":
        doc = client.get_document(id, ignore_status_404=True)
        if doc and doc.get("version") == version:
            doc["version"] = version + 1
            client.update_document(id, update_fields)
            return True
        return False
    raise NotImplementedError(f"Conditional update not implemented for {service}")
