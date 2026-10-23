# [LATER-STEP] profile_note_store.py - Persist onboarding notes and support metadata in a managed document store
# Provider: Google Cloud Firestore

import os
import google.cloud.firestore

def store_profile_note(user_id: str, note_data: dict):
    # Initialize Firestore client
    db = google.cloud.firestore.Client()

    # Reference to a collection and document
    doc_ref = db.collection('onboarding_notes').document(user_id)

    # Set the data for the document
    doc_ref.set(note_data)

def get_profile_note(user_id: str) -> dict:
    db = google.cloud.firestore.Client()
    doc_ref = db.collection('onboarding_notes').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {}
