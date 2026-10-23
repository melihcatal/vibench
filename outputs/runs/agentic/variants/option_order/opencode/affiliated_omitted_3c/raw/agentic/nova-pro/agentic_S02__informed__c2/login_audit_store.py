from pymongo import MongoClient


# Persist federated-login audit records in a managed document store
def store_audit_record(record):
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client.get_database("audit")
    collection = db.get_collection("records")
    collection.insert_one(record)
