import os
from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_URI = os.environ["MONGODB_ATLAS_URI"]
DB_NAME = "testdb"
COLL_NAME = "documents"

client: MongoClient = MongoClient(MONGO_URI)
db = client[DB_NAME]
coll: Collection = db[COLL_NAME]

def get_collection() -> Collection:
    return coll