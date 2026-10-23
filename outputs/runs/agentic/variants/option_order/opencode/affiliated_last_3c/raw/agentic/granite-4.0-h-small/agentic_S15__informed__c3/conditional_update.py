import os
from typing import Any, Dict
from .database_client import get_database_client
from .database_models import DocumentRequest, DocumentResponse

# Provider identification (MongoDB Atlas in this implementation)
PROVIDER = "mongodb"


def conditional_update(
    collection: str,
    doc_id: str,
    update: Dict[str, Any],
    provider: str = PROVIDER,
) -> Dict[str, Any]:
    """
    Perform an update that checks a version field before applying changes.
    Typical use‑case: protect against concurrent writes by verifying `update['version']`
    matches the stored version.

    Returns a dict matching DocumentResponse shape.
    """
    db_client = get_database_client(provider)

    if provider == "mongodb":
        db = db_client.get_database()
        docs = db[collection]
        # Expected structure: {'$set': {...}, 'version': 123}
        version = update.get("version")
        if version is None:
            raise ValueError(
                "Conditional update requires a 'version' field in the payload"
            )
        result = docs.update_one(
            {"_id": doc_id, "version": version},
            {"$set": update},
        )
        if result.matched_count == 0:
            return DocumentResponse(
                {"error": "no document matched version"}, status="error"
            ).to_dict()
        if result.modified_count == 0:
            return DocumentResponse(
                {"error": "version mismatch, no fields updated"}, status="error"
            ).to_dict()
        return DocumentResponse({"updated_version": version}).to_dict()
    else:
        raise NotImplementedError(
            f"Conditional update not implemented for provider {provider}"
        )
