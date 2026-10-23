# [SAME-SCENARIO] upsert_document.py

import json

# Import the Firestore client helper defined in database_client.py
from database_client import get_firestore_client

# Example: using Firestore as the managed NoSQL document store
# Identifier: Service = Cloud Firestore, SDK = google-cloud-firestore

# Document schema (simple example)
# {
#     'id': str,
#     'title': str,
#     'content': str,
#     'timestamp': str   # ISO 8601 string
# }


def upsert_document(doc: dict) -> None:
    """Upsert a JSON document into Firestore identified by its primary 'id'.

    The function creates the document if it does not exist, or replaces the
    existing document with the new payload.

    Args:
        doc (dict): Document payload with required 'id' field.
    """
    # Obtain a Firestore client (handles credential via GOOGLE_APPLICATION_CREDENTIALS)
    db = get_firestore_client()
    coll = db.collection("documents")  # root collection name
    doc_ref = coll.document(doc["id"])
    # Direct replace/write using set() with merge=True for upsert behavior
    doc_ref.set(doc, merge=True)
    print(f"Upserted (or created) document with id: {doc['id']}")
