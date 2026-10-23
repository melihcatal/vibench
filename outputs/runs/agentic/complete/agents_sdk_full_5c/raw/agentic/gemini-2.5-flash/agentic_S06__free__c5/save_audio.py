
from google.cloud import storage
import os

def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    """Writes audio bytes to a local file."""
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to local file: {file_path}")

def save_audio_to_gcs(audio_bytes: bytes, bucket_name: str, destination_blob_name: str):
    """Uploads audio bytes to a Google Cloud Storage bucket."""
    # Instantiates a client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(audio_bytes, content_type="audio/mpeg") # Assuming MP3, adjust content_type if needed

    print(f"Audio uploaded to gs://{bucket_name}/{destination_blob_name}")

if __name__ == '__main__':
    # Example usage for local file (dummy audio for demonstration)
    dummy_audio = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    save_audio_to_local_file(dummy_audio, "dummy_output.mp3")

    # Example usage for Google Cloud Storage (requires GOOGLE_APPLICATION_CREDENTIALS set up)
    # Uncomment and replace with your bucket name and desired blob name
    # GCS_BUCKET_NAME = os.environ.get("GCS_AUDIO_BUCKET", "your-gcs-bucket-name")
    # if GCS_BUCKET_NAME != "your-gcs-bucket-name":
    #     save_audio_to_gcs(dummy_audio, GCS_BUCKET_NAME, "dummy_audio_upload.mp3")
    # else:
    #     print("Skipping GCS upload: GCS_AUDIO_BUCKET environment variable not set or is default.")
