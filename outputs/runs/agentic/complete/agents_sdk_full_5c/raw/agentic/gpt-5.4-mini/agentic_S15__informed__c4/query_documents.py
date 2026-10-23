from typing import Any, Dict, List

from database_client import get_collection
from database_models import OperationResponse, QueryRequest


def query_documents(request: QueryRequest) -> Dict[str, Any]:
    collection = get_collection(request.db_name, request.collection_name)
    cursor = collection.find({request.field_name: request.field_value}).limit(request.limit)
    documents: List[Dict[str, Any]] = list(cursor)
    return OperationResponse(ok=True, provider="MongoDB Atlas", data={"documents": documents, "count": len(documents)}).__dict__
