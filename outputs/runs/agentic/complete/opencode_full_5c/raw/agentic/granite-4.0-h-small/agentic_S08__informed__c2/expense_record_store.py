# [LATER-STEP] expense_record_store.py

# Persists normalized expense records in MongoDB Atlas

import os
from pymongo import MongoClient
from bson.json_util import dumps

tls_ca_file = "./mongodb-atlas-ca.pem"

assert "MONGODB_ATLAS_URI" in os.environ, "Set MONGODB_ATLAS_URI"
assert "MONGODB_ATLAS_APIKEY" in os.environ, "Set MONGODB_ATLAS_APIKEY"

uri = os.getenv("MONGODB_ATLAS_URI")
client = MongoClient(uri, tlsCAFile=tls_ca_file)


def store_expense(record: dict, collection_name: str = "expenses"):
    """Insert a normalized expense record into MongoDB Atlas."""
    db = client.get_default_database()
    collection = db[collection_name]
    result = collection.insert_one(record)
    print(f"Stored expense with _id: {result.inserted_id}")
