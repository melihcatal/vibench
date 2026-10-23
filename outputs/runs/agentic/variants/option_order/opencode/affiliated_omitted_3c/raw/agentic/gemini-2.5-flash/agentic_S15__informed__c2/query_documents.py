import os
from typing import Any, Dict, List
from database_client import MongoDBClient
from database_models import Document, DocumentQuery


def query_documents(query: DocumentQuery) -> List[Document]:
    collection = MongoDBClient.get_collection()
    results = collection.find({query.field: query.value})
    return [Document.from_dict(data) for data in results]
