import os
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional

MONGO_URI: Optional[str] = os.getenv("MONGODB_ATLAS_URI")
if not MONGO_URI:
    raise ValueError(
        "Environment variable MONGODB_ATLAS_URI must be set for MongoDB Atlas."
    )

_client = MongoClient(MONGO_URI)
db = _client["testdb"]
_collection: Collection = db["documents"]


def get_collection() -> Collection:
    return _collection
