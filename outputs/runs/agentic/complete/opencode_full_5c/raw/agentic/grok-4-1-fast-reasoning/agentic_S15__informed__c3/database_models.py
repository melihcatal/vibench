from typing import Dict, Any, Optional


def normalize_from_storage(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if doc is None:
        return None
    result = doc.copy()
    result["id"] = str(result.pop("_id"))
    return result
