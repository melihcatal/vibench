import os
from google.cloud import firestore


def message_audit_store(message):
    client = firestore.Client()
    collection_ref = client.collection("message_audit")
    collection_ref.add({"message": message})
    print("Message stored in audit store")
