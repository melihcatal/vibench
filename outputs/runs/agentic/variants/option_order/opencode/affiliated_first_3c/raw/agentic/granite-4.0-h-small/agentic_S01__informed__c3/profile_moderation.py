import os
from google.cloud import storage

client = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

BLOB_PATH = 'onboarding/metadata/'.

def moderate_profile_text(text):
    """Moderate profile text before account activation.
    Uses placeholder moderation (e.g., profanity filter) and returns cleaned text.
    """
    # Placeholder moderation logic - replace with real moderation service call if needed
    return text.strip()


def persist_onboarding_notes(note_id, content):
    """Persist onboarding notes and metadata in Google Cloud Storage.
    Returns blob URL.
    """
    bucket = client.get_bucket('my-onboarding-bucket')
    blob = bucket.blob(f'{BLOB_PATH}{note_id}.json')
    blob.upload_from_string(content)
    return blob.public_url

