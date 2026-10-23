import os
from google.cloud import storage
from typing import Union

def save_audio(
    audio_content: bytes,
    destination_path: str,
    bucket_name: str = None,
) -> None:
    """Saves audio content to a local file or Google Cloud Storage."""
    if bucket_name:
        # Save to Google Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_path)
        blob.upload_from_string(audio_content, content_type="audio/mpeg")
        print(f"Audio saved to gs://{bucket_name}/{destination_path}")
    else:
        # Save to local file
        with open(destination_path, "wb") as out:
            out.write(audio_content)
        print(f"Audio saved to local file: {destination_path}")

if __name__ == '__main__':
    # Example local usage
    sample_audio_bytes = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    local_file_path = "output_audio.mp3"
    save_audio(sample_audio_bytes, local_file_path)

    # Example GCS usage (uncomment and replace with your bucket/path)
    # GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    # if GCS_BUCKET_NAME:
    #     gcs_object_path = "synthesized_audio/test_gcs_audio.mp3"
    #     save_audio(sample_audio_bytes, gcs_object_path, bucket_name=GCS_BUCKET_NAME)
    # else:
    #     print("GCS_BUCKET_NAME environment variable not set. Skipping GCS example.")
