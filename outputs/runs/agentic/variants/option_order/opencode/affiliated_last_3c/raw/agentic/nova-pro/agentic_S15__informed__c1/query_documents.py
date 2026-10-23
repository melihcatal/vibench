import os
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()


def query_documents(field, value):
    docs = db.collection("documents").where(field, "==", value).stream()
    return [doc.to_dict() for doc in docs]
