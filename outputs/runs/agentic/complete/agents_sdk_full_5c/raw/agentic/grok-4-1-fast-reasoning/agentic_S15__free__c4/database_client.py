import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

uri = os.environ.get('MONGODB_ATLAS_URI')
if not uri:
    raise ValueError("MONGODB_ATLAS_URI environment variable is required")

mongo_client = MongoClient(uri)
db_name = os.environ.get('MONGODB_DB_NAME', 'testdb')
collection_name = os.environ.get('MONGODB_COLLECTION_NAME', 'documents')
db = mongo_client[db_name]
coll = db[collection_name]