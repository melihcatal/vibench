from pymongo import MongoClient

def login_audit_store(audit_record):
    client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/test')
    db = client.test
    collection = db.audit_records
    collection.insert_one(audit_record)