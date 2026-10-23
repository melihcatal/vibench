import pymongo

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")


def persist_audit_records(records):
    client = pymongo.MongoClient(MONGODB_ATLAS_URI)
    db = client.audit_logs
    collection = db.records
    collection.insert_many(records)
    return "Audit records persisted"
