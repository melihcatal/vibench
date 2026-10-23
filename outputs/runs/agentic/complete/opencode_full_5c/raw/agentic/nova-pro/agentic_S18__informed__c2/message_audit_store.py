import os
from google.cloud import firestore

db = firestore.Client()


def message_audit_store(message):
    db.collection("messages").add(message)
