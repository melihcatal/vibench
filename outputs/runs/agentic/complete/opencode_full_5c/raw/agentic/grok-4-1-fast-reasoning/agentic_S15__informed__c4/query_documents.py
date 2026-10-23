from typing import Any, List, Dict
from database_client import get_collection
from database_models import normalize_documents


def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    cursor = get_collection().find({field_name: field_value})
    docs = list(cursor)
    return normalize_documents(docs)
