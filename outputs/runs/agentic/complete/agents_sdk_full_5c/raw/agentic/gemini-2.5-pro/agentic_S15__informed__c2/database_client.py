import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# It's recommended to use a centralized configuration management system
# instead of environment variables in a production environment.
MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI")

if not MONGODB_ATLAS_URI:
    raise ValueError("MONGODB_ATLAS_URI environment variable not set")

_client = MongoClient(MONGODB_ATLAS_URI)

# Centralized function to get the database and collection
def get_db_collection(
    db_name: str = "main_db", collection_name: str = "documents"
) -> Collection:
    """
    Returns a handle to a MongoDB collection.
    """
    db: Database = _client[db_name]
    collection: Collection = db[collection_name]
    return collection
