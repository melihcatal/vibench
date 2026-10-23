import os
from google.cloud import firestore

db = firestore.Client(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

def store_audit_record(record):
    db.collection(u'audit_logs').add(record)