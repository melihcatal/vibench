import json
from google.cloud import firestore


def store_message_audit(record):
    client = firestore.Client()
    doc = client.collection('message_audit').document(str(record.get('id', 'unknown')))
    doc.set(record)
    return json.dumps({'stored': True, 'id': record.get('id', 'unknown')}, sort_keys=True)
