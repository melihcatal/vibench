from typing import Dict, Any, Optional
from database_client import get_collection

def conditional_update(document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None) -> bool:
    filter_criteria = {'_id': document_id}
    if expected_version is not None:
        filter_criteria['version'] = expected_version
    update_ops = {'$set': updates}
    if expected_version is not None:
        update_ops['$inc'] = {'version': 1}
    collection = get_collection()
    result = collection.update_one(filter_criteria, update_ops)
    return result.modified_count > 0