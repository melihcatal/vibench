import os
import pymongo

MONGODB_ATLAS_URI = os.getenv('MONGODB_ATLAS_URI')

def store_login_audit(audit_record):
    client = pymongo.MongoClient(MONGODB_ATLAS_URI)
    db = client.login_audit
    collection = db.audit_records
    collection.insert_one(audit_record)
    print('Audit record stored successfully')