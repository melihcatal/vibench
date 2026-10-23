# message_audit_store.py
# [LATER-STEP]
# Persist processed Pub/Sub messages to Google Firestore for later lookup.

import os
from google.cloud import firestore
from .messaging_models import EventMessage

def store_message(message: EventMessage) -> None:
    """Write a normalized message document to Firestore collection 'processed_messages'.

    The document ID will be the Pub/Sub message ID. Fields include original topic, payload, and attributes.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var for auth
    doc_ref = db.collection('processed_messages').document(message.message_id)
    doc_data = {
        'original_topic': message.attributes.get('original_topic', '<unknown>'),
        'published_at': message.publish_time,
        'payload': message.to_event_payload().data,
        'attributes': message.attributes,
    }
    doc_ref.set(doc_data)
