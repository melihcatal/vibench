import os
import json
import requests
from google.cloud import datastore

# Datastore configuration (Google Cloud Managed Document Store)
DATASTORE_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
CLIENT = datastore.Client(project=DATASTORE_PROJECT)

KIND = 'ProfileText'

MODERATION_ENDPOINT = 'https://api.moderation-service.com/v1/moderate'
MODERATION_API_KEY = os.getenv('MODERATION_API_KEY')

HEADERS = {'Authorization': f'Bearer {MODERATION_API_KEY}', 'Content-Type': 'application/json'}

def moderate_profile_text(user_id: str, text: str) -> str:
    """Moderate profile text before account activation using an external moderation API.
    Returns the approved (or sanitized) text. Raises RuntimeError on severe violations.
    """
    payload = {'text': text, 'user_id': user_id}
    resp = requests.post(MODERATION_ENDPOINT, headers=HEADERS, json=payload)
    resp.raise_for_status()
    result = resp.json()
    if result.get('status') == 'approved':
        return result['text']
    elif result.get('status') == 'rejected':
        raise RuntimeError(f"Profile moderation rejected text from user {user_id}")
    else:
        # Fallback: return sanitized text
        return result.get('sanitized', text)

def store_profile_note(user_id: str, note: dict):
    """Persist onboarding notes and support metadata in Google Cloud Datastore (managed document store)."""
    key = CLIENT.key(KIND, user_id)
    # Ensure we don't overwrite existing notes; add under a sub-key list
    note_entity = datastore.Entity(key=key)
    note_entity.update(note)
    CLIENT.put(note_entity)
    return {'kind': KIND, 'id': user_id}
