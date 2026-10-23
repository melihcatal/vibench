from pymongo import MongoClient, ReturnDocument
from pymongo.errors import PyMongoError
import os
from typing import Dict, Any, Optional
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


class ConditionalDocumentUpdater:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_ATLAS_DB_NAME", "documents")]
        self.collection = self.db[
            os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "documents")
        ]

    def update(self, request: ConditionalUpdateRequest) -> ConditionalUpdateResponse:
        try:
            query = {"_id": request.document_id}
            if request.current_version:
                query["version"] = request.current_version

            update_doc = {"$set": request.updates}
            if request.new_version:
                update_doc["$set"]["version"] = request.new_version

            result = self.collection.find_one_and_update(
                query, update_doc, return_document=ReturnDocument.AFTER
            )

            if result:
                return ConditionalUpdateResponse(success=True, document=result)
            return ConditionalUpdateResponse(
                success=False, error="Document not found or version mismatch"
            )
        except PyMongoError as e:
            return ConditionalUpdateResponse(success=False, error=str(e))
