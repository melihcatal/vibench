import os
from google.cloud import firestore

db = firestore.Client()

def store_message(message):
    doc_ref = db.collection(u'messages').document()
    doc_ref.set(message)