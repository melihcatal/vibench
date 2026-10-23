import os
from google.cloud import firestore

def save_onboarding_note(user_id: str, note_content: str, metadata: dict):
    """
    Persists onboarding notes and support metadata in Google Cloud Firestore.

    Args:
        user_id: The ID of the user the note is associated with.
        note_content: The content of the onboarding note.
        metadata: A dictionary containing additional support metadata.
    """
    # Initialize Firestore client
    # The project ID is typically inferred from the environment
    # (e.g., GOOGLE_CLOUD_PROJECT environment variable) or explicit configuration.
    # For explicit configuration, uncomment the line below and replace 'your-gcp-project-id'
    # db = firestore.Client(project='your-gcp-project-id')
    db = firestore.Client()

    # Create a reference to the 'onboarding_notes' collection
    doc_ref = db.collection('onboarding_notes').document(user_id)

    # Prepare the data to be stored
    note_data = {
        'note_content': note_content,
        'metadata': metadata,
        'timestamp': firestore.SERVER_TIMESTAMP
    }

    # Set the document data. If the document already exists, it will be updated.
    doc_ref.set(note_data, merge=True)
    