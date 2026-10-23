import os
from speech_client import get_storage_client

def save_audio_to_gcs(audio_content: bytes, bucket_name: str, destination_blob_name: str):
    """
    Saves audio content to a Google Cloud Storage bucket.

    Args:
        audio_content: The audio content as bytes.
        bucket_name: The name of the GCS bucket.
        destination_blob_name: The path/name of the file in the bucket.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_content, content_type='audio/mpeg') # Assuming MP3 for example
    print(f"Audio saved to gs://{bucket_name}/{destination_blob_name}")

def save_audio_to_local_file(audio_content: bytes, file_path: str):
    """
    Saves audio content to a local file.

    Args:
        audio_content: The audio content as bytes.
        file_path: The local file path to save the audio.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(audio_content)
    print(f"Audio saved to local file: {file_path}")
