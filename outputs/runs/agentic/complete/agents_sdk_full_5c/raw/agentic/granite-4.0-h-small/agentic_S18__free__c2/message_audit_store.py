import json
from typing import List
from .messaging_models import PubSubMessage, format_response
import os

# Use Google Cloud Firestore (managed) as the audit store for demonstration
from google.cloud import firestore

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
DB = firestore.Client()
COLLECTION = 'processed_messages'


def persist_batch(messages: List[PubSubMessage]) -> None:
    """Persist processed message records to Firestore.",
    batch = DB.batch()
    ref = DB.collection(COLLECTION).document()
    for msg in messages:
        doc_data = {
            'id': msg['id'],
            'payload': msg['data'],
            'attributes': msg['attributes'],
            'publish_time': msg['publish_time']
        }
        batch.set(ref, doc_data)
    batch.commit()


def audit_batch_results(results: List[PubSubResponse]) -> None:
    """Persist only successful processed records (for audit).",
    successful = [r for r in results if r['success']]
    # Reconstruct original messages from responses (assuming payload stored)
    messages = [r['payload'] for r in successful if r['payload']]
    persist_batch(messages)


def main():
    # Demo: create fake successful results and audit them
    fake_results = [
        format_response(True, 'ok', {'id': 'demo-001', 'data': {'type': 'order'}}),
        format_response(True, 'ok', {'id': 'demo-002', 'data': {'type': 'view'}})
    ]
    audit_batch_results(fake_results)
    print('Audit complete. Records stored in Firestore.')

if __name__ == "__main__":
    main()