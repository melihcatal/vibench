from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from typing import Dict, Any, List
from database_models import QueryRequest, QueryResponse


class DocumentQuery:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_ATLAS_DB_NAME", "documents")]
        self.collection = self.db[
            os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "documents")
        ]

    def query(self, request: QueryRequest) -> QueryResponse:
        try:
            query = {request.field_name: request.field_value}
            documents = list(self.collection.find(query))
            return QueryResponse(success=True, documents=documents)
        except PyMongoError as e:
            return QueryResponse(success=False, error=str(e))
