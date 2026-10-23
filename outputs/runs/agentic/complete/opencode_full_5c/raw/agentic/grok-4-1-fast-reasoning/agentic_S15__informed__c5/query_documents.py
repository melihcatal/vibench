from database_client import get_collection
from database_models import Document
from typing import Any, List


def query_documents(field: str, value: Any) -> List[Document]:
    collection = get_collection()
    return list(collection.find({field: value}))
