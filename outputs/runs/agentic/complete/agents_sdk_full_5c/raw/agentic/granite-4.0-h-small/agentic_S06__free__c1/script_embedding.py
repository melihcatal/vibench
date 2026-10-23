import os
import json
from google.cloud import storage
from google.cloud import speech
from .speech_models import SpeechSynthesisInput, SpeechSynthesisOutput

def embed_narration(script: str, bucket_name: str, object_name: str) -> str:
    """Embed a narration script into a cloud storage object for later voice-asset search.

    The function writes the script content to a GCS object and optionally creates a transcription
    (optional extension).
    Returns the public URL of the stored object.
    """
    # Write script to storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(script)
    # Make public (optional)
    blob.make_public()
    return f'https://storage.googleapis.com/{bucket_name}/{object_name}'
