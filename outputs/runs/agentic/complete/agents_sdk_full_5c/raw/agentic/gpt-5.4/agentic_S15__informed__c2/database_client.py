from __future__ import annotations

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
MONGODB_ATLAS_DATABASE = os.getenv("MONGODB_ATLAS_DATABASE", "app")
MONGODB_ATLAS_COLLECTION = os.getenv("MONGODB_ATLAS_COLLECTION", "documents")


_client: Optional[MongoClient] = None



def get_mongodb_client() -> MongoClient:
    global _client
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI is required for MongoDB Atlas")
    if _client is None:
        _client = MongoClient(MONGODB_ATLAS_URI, appname="managed-nosql-integration")
    return _client



def get_database() -> Database:
    return get_mongodb_client()[MONGODB_ATLAS_DATABASE]



def get_collection() -> Collection:
    return get_database()[MONGODB_ATLAS_COLLECTION]



def ensure_indexes() -> Collection:
    collection = get_collection()
    collection.create_index("partition_key")
    collection.create_index("version")
    collection.create_index("updated_at")
    return collection
