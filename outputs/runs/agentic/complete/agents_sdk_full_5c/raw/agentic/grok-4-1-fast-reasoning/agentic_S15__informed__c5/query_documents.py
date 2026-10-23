from database_client import get_collection
from database_models import Documents
from typing import Any

def query_documents(field_name: str, value: Any) -> Documents:
    coll = get_collection()
    return list(coll.find({field_name: value}))
