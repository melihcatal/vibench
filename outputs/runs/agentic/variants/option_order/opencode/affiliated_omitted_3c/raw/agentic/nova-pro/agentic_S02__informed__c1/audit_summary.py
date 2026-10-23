import pymongo

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")


def summarize_audit_events(events):
    client = pymongo.MongoClient(MONGODB_ATLAS_URI)
    db = client.audit_logs
    collection = db.events
    collection.insert_many(events)
    return "Audit events summarized"
