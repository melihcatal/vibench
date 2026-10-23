from typing import Any, Dict

from database_client import get_collection
from database_models import OperationResponse


def fetch_document(document_id: Any, db_name: str = None, collection_name: str = None) -> Dict[str, Any]:
    collection = get_collection(db_name, collection_name)
    document = collection.find_one({"_id": str(document_id)})
    return OperationResponse(ok=document is not None, provider="MongoDB Atlas", data={"document": document}).__dict__
