import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_ATLAS_URI environment variable is required")

client = MongoClient(MONGO_URI)
db = client["documents_db"]
collection = db["documents"]


def get_collection():
    return collection
