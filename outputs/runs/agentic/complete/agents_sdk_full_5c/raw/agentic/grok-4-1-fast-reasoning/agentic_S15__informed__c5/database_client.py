import os
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymongo.collection import Collection

MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_ATLAS_URI environment variable is required")

client = MongoClient(MONGO_URI)
db = client["documentdb"]
coll: "Collection" = db["documents"]

def get_collection() -> "Collection":
    return coll
