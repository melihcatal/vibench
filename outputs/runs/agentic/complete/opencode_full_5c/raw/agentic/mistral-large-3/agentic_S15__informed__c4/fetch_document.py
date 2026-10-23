from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from typing import Dict, Any, Optional
from database_models import FetchRequest, FetchResponse


class DocumentFetcher:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_ATLAS_DB_NAME", "documents")]
        self.collection = self.db[
            os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "documents")
        ]

    def fetch(self, request: FetchRequest) -> FetchResponse:
        try:
            document = self.collection.find_one({"_id": request.document_id})
            if document:
                return FetchResponse(success=True, document=document)
            return FetchResponse(success=False, error="Document not found")
        except PyMongoError as e:
            return FetchResponse(success=False, error=str(e))
