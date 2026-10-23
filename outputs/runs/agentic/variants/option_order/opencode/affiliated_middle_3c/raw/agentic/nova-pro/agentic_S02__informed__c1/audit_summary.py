import os
from google.cloud import firestore

# Configuration
db = firestore.Client()


# Summarize federated-login audit events
def summarize_audit_events():
    audit_collection = db.collection("audit_events")
    summary = audit_collection.aggregate([("count", firestore.aggregate.COUNT)]).get()
    return summary
