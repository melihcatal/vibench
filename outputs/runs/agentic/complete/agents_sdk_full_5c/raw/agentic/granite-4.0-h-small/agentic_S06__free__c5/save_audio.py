# save_audio.py
# [SAME-SCENARIO] Writes synthesized speech audio to a local file or object storage (e.g., Google Cloud Storage) using Google Cloud Text-to-Speech.

import os
from typing import Union
from google.cloud import texttospeech, storage
from speech_client import get_texttospeech_client

def download_to_local(audio_bytes: bytes, local_path: str):
    """Save audio bytes to a local file.

    Args:
        audio_bytes: Raw audio content from TTS synthesis.
        local_path: Destination file path.
    """
    with open(local_path, 'wb') as f:
        f.write(audio_bytes)
    print(f'Audio saved locally to {local_path}')


def upload_to_gcs(audio_bytes: bytes, bucket_name: str, blob_name: str):
    """Upload audio bytes to Google Cloud Storage.

    Args:
        audio_bytes: Raw audio content.
        bucket_name: GCS bucket identifier.
        blob_name: Object name/path within the bucket.
    """
    client = get_texttospeech_client()  # Reuse credentials
    bucket = storage.Client().bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(audio_bytes, content_type='audio/mpeg')
    print(f'Audio uploaded to gs://{bucket_name}/{blob_name}')


def save_audio(audio_bytes: bytes, destination: Union[str, tuple], *, bucket_name: str = None, blob_name: str = None):
    """Generic audio saver that supports local file or GCS bucket.

    Usage:
        - Local file: save_audio(audio_bytes, 'output.mp3')
        - GCS: save_audio(audio_bytes, ('gs_bucket', 'object.mp3'), bucket_name='my-bucket')
    """
    if isinstance(destination, str):
        # Local file path
        download_to_local(audio_bytes, destination)
    elif isinstance(destination, tuple) and len(destination) == 2 and destination[0] == 'gs':
        # GCS target: ( 'gs', 'object.mp3' )
        if not bucket_name:
            raise ValueError('bucket_name must be provided for GCS destination')
        upload_to_gcs(audio_bytes, bucket_name, blob_name=destination[1])
    else:
        raise ValueError('Invalid destination format')
