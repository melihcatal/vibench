from google.cloud import firestore

# Configuration
PROJECT_ID = 'your-project-id'

# Initialize client
client = firestore.Client(project=PROJECT_ID)

# Function to persist onboarding notes
def persist_onboarding_notes(user_id, notes):
    doc_ref = client.collection(u'onboarding_notes').document(user_id)
    doc_ref.set({
        'notes': notes,
        'timestamp': firestore.SERVER_TIMESTAMP,
    })