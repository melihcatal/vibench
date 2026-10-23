from database_client import get_collection
from database_models import prepare_update_pipeline
from typing import Dict, Any, Optional


def conditional_update(
    doc_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None
) -> bool:
    collection = get_collection()
    filter_dict = {"_id": doc_id}
    if expected_version is not None:
        filter_dict["version"] = expected_version
    pipeline = prepare_update_pipeline(updates)
    updated = collection.find_one_and_update(
        filter_dict, pipeline, return_document=True
    )
    return updated is not None
