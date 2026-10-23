from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
from typing import Dict, Any, Optional
from database_models import UpsertRequest, UpsertResponse


class DocumentUpserter:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_ATLAS_DB_NAME", "documents")]
        self.collection = self.db[
            os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "documents")
        ]

    def upsert(self, request: UpsertRequest) -> UpsertResponse:
        try:
            result = self.collection.replace_one(
                {"_id": request.document_id}, request.document, upsert=True
            )
            return UpsertResponse(
                success=True,
                document_id=request.document_id,
                version=str(result.upserted_id or request.document.get("_id")),
            )
        except PyMongoError as e:
            return UpsertResponse(
                success=False, document_id=request.document_id, error=str(e)
            )
