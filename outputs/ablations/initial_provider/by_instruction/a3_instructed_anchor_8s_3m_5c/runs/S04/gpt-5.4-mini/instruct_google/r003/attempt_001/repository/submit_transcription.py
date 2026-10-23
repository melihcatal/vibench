import os
from typing import Any, Dict

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage

from speech_client import build_google_speech_config, get_default_bucket, get_project_id


def _upload_to_gcs(client: storage.Client, audio_path: str, bucket_name: str) -> str:
    bucket = client.bucket(bucket_name)
    blob_name = os.path.basename(audio_path)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(audio_path)
    return f"gs://{bucket_name}/{blob_name}"


def submit_transcription(audio_path: str, language_code: str = "en-US") -> Dict[str, Any]:
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    storage_client = storage.Client(project=project_id)
    bucket_name = get_default_bucket()
    if not bucket_name:
        raise ValueError("GOOGLE_CLOUD_STORAGE_BUCKET is required")
    gcs_uri = _upload_to_gcs(storage_client, audio_path, bucket_name)
    client = speech.SpeechClient()
    request = {
        "config": build_google_speech_config({"language_code": language_code}),
        "audio": {"uri": gcs_uri},
    }
    operation = client.long_running_recognize(request=request)
    return {"job_name": operation.operation.name, "audio_uri": gcs_uri, "provider": "google"}
