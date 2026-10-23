from pymongo import MongoClient


# Persist federated-login audit records in a managed document store
def store_audit_record(record):
    client = MongoClient("your-mongodb-uri")
    db = client["audit_db"]
    collection = db["audit_records"]
    collection.insert_one(record)
