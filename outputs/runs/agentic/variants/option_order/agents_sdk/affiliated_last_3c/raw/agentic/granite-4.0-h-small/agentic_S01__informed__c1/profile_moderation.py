import os
import json
from typing import Dict, Any
from google.cloud import storage
from identity_models import RegisterRequest

# Using Google Cloud Storage as a managed document store for moderation metadata
# Environment variables expected: GOOGLE_APPLICATION_CREDENTIALS, BUCKET_NAME

bucket_name = os.getenv('BUCKET_NAME')
if not bucket_name:
    raise RuntimeError('BUCKET_NAME environment variable not set')

storage_client = storage.Client()

MODERATION_PREFIX = 'moderation/'

IDENTITY_DATA_KEY = 'identity_data.json'

# In-memory store for profile text, should be replaced with real I/O after user confirmation
global_profile_text = {}

def moderate_profile(user_id: str, raw_text: str, locale: str) -> str:
    """Moderate profile text before account activation.","""    # Placeholder moderation logic: strip HTML tags, limit length, replace disallowed words
    moderated = ''.join(raw_text.split()).strip()[:500]  # simple trimming
    # Persist original and moderated version alongside identity data
    identity_data: Dict[str, Any] = {
        'user_id': user_id,
        'locale': locale,
        'raw_text': raw_text,
        'moderated_text': moderated
    }
    store_identity_data(user_id, identity_data)
    # Store in GCS for audit
    doc_id = f"{MODERATION_PREFIX}{user_id}" 
    blob = storage_client.bucket(bucket_name).blob(doc_id)
    blob.upload_from_string(json.dumps(identity_data))
    return moderated

def store_identity_data(user_id: str, data: Dict[str, Any]):
    """Persist identity-related notes and metadata in GCS.","""    blob = storage_client.bucket(bucket_name).blob(f"{IDENTITY_DATA_KEY}/{user_id}.json")
    blob.upload_from_string(json.dumps(data))


# Helper to fetch stored moderation for support tools

def fetch_moderation(user_id: str) -> Dict[str, Any]:
    blob = storage_client.bucket(bucket_name).blob(f"{MODERATION_PREFIX}{user_id}")
    if not blob.exists():
        raise FileNotFoundError(f"Moderation record not found for {user_id}")
    return json.loads(blob.download_as_string())
