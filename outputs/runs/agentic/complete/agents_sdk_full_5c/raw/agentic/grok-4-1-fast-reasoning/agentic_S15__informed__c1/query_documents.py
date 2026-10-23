from typing import Any, List
from database_client import get_collection
from database_models import Document

def query_documents(field: str, value: Any) -> List[Document]:
    return list(get_collection().find({field: value}))