from speech_models import SynthesisResponse
import os

def save_audio_to_file(response: SynthesisResponse, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as audio_file:
        audio_file.write(response.audio_content)

def save_audio_to_gcs(response: SynthesisResponse, bucket_name: str, blob_name: str) -> None:
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(response.audio_content, content_type="audio/mpeg")