import os
import pymongo
from datetime import datetime
from identity_models import AuditRecord

def store_audit_record(record: AuditRecord) -> str:
    mongodb_uri = os.environ.get("MONGODB_URI")
    mongodb_db_name = os.environ.get("MONGODB_DB_NAME", "federated_login_audits")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable not set.")
    
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db_name]
    
    audits_collection = db.login_audits
    
    record_dict = dict(record)
    if 'timestamp' in record_dict and isinstance(record_dict['timestamp'], str):
        record_dict['timestamp'] = datetime.fromisoformat(record_dict['timestamp'])

    insert_result = audits_collection.insert_one(record_dict)
    
    client.close()
    return str(insert_result.inserted_id)
