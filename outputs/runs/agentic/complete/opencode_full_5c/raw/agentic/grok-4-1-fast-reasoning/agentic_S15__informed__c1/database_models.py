from typing import Dict, Any, List, Optional

Document = Dict[str, Any]
Documents = List[Document]


def prepare_update_pipeline(updates: Dict[str, Any]) -> list[dict]:
    return [{"$set": {**updates, "version": {"$ifNull": ["$version", 0]} + 1}}]
