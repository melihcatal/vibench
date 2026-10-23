from pymongo import MongoClient
from identity_client import get_mongodb_config
from identity_models import AuditRecord
import datetime

def store_audit_record(record: AuditRecord):
    mongo_config = get_mongodb_config()
    mongo_uri = mongo_config["MONGO_URI"]
    db_name = mongo_config["MONGO_DB_NAME"]
    collection_name = mongo_config["MONGO_COLLECTION_NAME"]

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Convert AuditRecord to a dictionary for MongoDB insertion
    record_dict = record.__dict__
    # Ensure timestamp is in ISO format if not already
    if isinstance(record_dict.get("timestamp"), datetime.datetime):
        record_dict["timestamp"] = record_dict["timestamp"].isoformat()

    collection.insert_one(record_dict)
    client.close()
