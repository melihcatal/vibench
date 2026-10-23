import os
from functools import lru_cache

from pymongo import MongoClient


DATABASE_NAME = os.getenv("MONGODB_ATLAS_DATABASE", "document_store")
COLLECTION_NAME = os.getenv("MONGODB_ATLAS_COLLECTION", "documents")


def _get_uri() -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI is required")
    return uri


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    return MongoClient(_get_uri())


def get_collection():
    return get_client()[DATABASE_NAME][COLLECTION_NAME]
