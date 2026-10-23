from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from database_models import DocumentRequest, QueryRequest, UpdateRequest, merge_updates, normalize_document

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_ATLAS_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_ATLAS_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"
DEFAULT_DB_NAME = "documents"
DEFAULT_COLLECTION_NAME = "records"


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    mongo_uri = uri or os.getenv(MONGODB_ATLAS_URI_ENV)
    if not mongo_uri:
        raise RuntimeError(f"Missing MongoDB Atlas connection string in {MONGODB_ATLAS_URI_ENV}")
    return MongoClient(mongo_uri)


def get_database(client: MongoClient, db_name: Optional[str] = None) -> Database:
    return client[db_name or os.getenv(MONGODB_ATLAS_DB_ENV, DEFAULT_DB_NAME)]


def get_collection(client: MongoClient, collection_name: Optional[str] = None, db_name: Optional[str] = None) -> Collection:
    database = get_database(client, db_name=db_name)
    return database[collection_name or os.getenv(MONGODB_ATLAS_COLLECTION_ENV, DEFAULT_COLLECTION_NAME)]


class ManagedDocumentStore:
    def __init__(self, client: Optional[MongoClient] = None, db_name: Optional[str] = None, collection_name: Optional[str] = None) -> None:
        self.client = client or get_mongo_client()
        self.collection = get_collection(self.client, collection_name=collection_name, db_name=db_name)

    def upsert(self, request: DocumentRequest) -> Dict[str, Any]:
        normalized = normalize_document({**request.payload, "id": request.document_id})
        filter_doc = {"_id": normalized.document_id}
        if request.partition_key is not None:
            filter_doc["partition_key"] = request.partition_key
        result = self.collection.replace_one(filter_doc, {**normalized.body, "_id": normalized.document_id}, upsert=True)
        return {"document_id": normalized.document_id, "matched_count": result.matched_count, "modified_count": result.modified_count, "upserted_id": str(result.upserted_id) if result.upserted_id is not None else normalized.document_id}

    def fetch(self, document_id: str, partition_key: Optional[str] = None) -> Dict[str, Any]:
        filter_doc = {"_id": document_id}
        if partition_key is not None:
            filter_doc["partition_key"] = partition_key
        doc = self.collection.find_one(filter_doc)
        if not doc:
            raise KeyError(document_id)
        doc["id"] = str(doc.pop("_id"))
        return doc

    def query(self, request: QueryRequest) -> Iterable[Dict[str, Any]]:
        query: Dict[str, Any] = {request.field_name: request.field_value}
        if request.partition_key is not None:
            query["partition_key"] = request.partition_key
        cursor = self.collection.find(query).limit(request.limit)
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            yield doc

    def conditional_update(self, request: UpdateRequest) -> Dict[str, Any]:
        filter_doc: Dict[str, Any] = {"_id": request.document_id}
        if request.etag is not None:
            filter_doc["etag"] = request.etag
        if request.partition_key is not None:
            filter_doc["partition_key"] = request.partition_key
        existing = self.collection.find_one(filter_doc)
        if not existing:
            raise KeyError(request.document_id)
        updated = merge_updates(existing, request.updates)
        new_etag = request.etag or existing.get("etag")
        if new_etag is not None:
            updated["etag"] = new_etag
        result = self.collection.replace_one(filter_doc, updated, upsert=False)
        return {"document_id": request.document_id, "matched_count": result.matched_count, "modified_count": result.modified_count}
