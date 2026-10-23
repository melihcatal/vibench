import os
from functools import lru_cache
from typing import Any, Dict

from pymongo import MongoClient


def get_config() -> Dict[str, Any]:
    return {
        "uri": os.environ.get("MONGODB_ATLAS_URI", ""),
        "database": os.environ.get("MONGODB_ATLAS_DATABASE", "documents"),
        "collection": os.environ.get("MONGODB_ATLAS_COLLECTION", "records"),
    }


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    cfg = get_config()
    return MongoClient(cfg["uri"])


def get_collection():
    cfg = get_config()
    return get_client()[cfg["database"]][cfg["collection"]]
