from database_client import get_collection
from database_models import Documents, Any

def query_documents(field: str, value: Any) -> Documents:
    coll = get_collection()
    return list(coll.find({field: value}))