import os
from google.cloud import firestore
from identity_client import get_google_project_id
from identity_models import OnboardingNote

def profile_note_store(note: OnboardingNote):
    project_id = get_google_project_id()
    db = firestore.Client(project=project_id)

    # Use a collection specific to onboarding notes
    collection_ref = db.collection("onboarding_notes")
    
    # Add a new document with an auto-generated ID
    # The note content is directly stored as document fields
    collection_ref.add(note)