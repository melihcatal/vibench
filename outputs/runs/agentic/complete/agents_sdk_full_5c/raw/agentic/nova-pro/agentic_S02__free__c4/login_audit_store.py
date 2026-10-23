from pymongo import MongoClient

def store_audit_record(record):
    client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority')
    db = client.test
    collection = db.audit_logs
    collection.insert_one(record)