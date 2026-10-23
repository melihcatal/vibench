import os
from functools import lru_cache
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_client():
    return MongoClient(os.environ["MONGODB_ATLAS_URI"])


def get_database():
    return get_client()[os.getenv("MONGODB_ATLAS_DB", "documents")]


def get_collection():
    return get_database()[os.getenv("MONGODB_ATLAS_COLLECTION", "records")]
