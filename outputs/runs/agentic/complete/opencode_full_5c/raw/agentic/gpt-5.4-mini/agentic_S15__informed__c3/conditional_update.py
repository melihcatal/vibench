from typing import Any, Dict, Optional

from database_client import get_collection


def conditional_update(
    identifier: str, patch: Dict[str, Any], version: Optional[int] = None
) -> Dict[str, Any]:
    collection = get_collection()
    criteria = {"_id": str(identifier)}
    if version is not None:
        criteria["version"] = version
        patch = dict(patch)
        patch["version"] = version + 1
    result = collection.update_one(criteria, {"$set": patch})
    return {
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


def handler(
    identifier: str, patch: Dict[str, Any], version: Optional[int] = None
) -> Dict[str, Any]:
    return conditional_update(identifier, patch, version)
