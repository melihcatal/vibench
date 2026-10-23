import os
from google.cloud import firestore

# Configuration
db = firestore.Client()


# Persist federated-login audit records in a managed document store
def store_audit_record(record):
    audit_collection = db.collection("audit_records")
    audit_collection.add(record)
