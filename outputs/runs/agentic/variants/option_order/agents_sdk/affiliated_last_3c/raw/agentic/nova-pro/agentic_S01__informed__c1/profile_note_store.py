import os
from google.cloud import firestore

# Google Firestore setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize Google Firestore client
db = firestore.Client()

# Function to store onboarding notes
def store_note(user_id, note):
    doc_ref = db.collection('users').document(user_id)
    doc_ref.set({'onboarding_note': note})
    return doc_ref.id