from google.cloud import storage
import os

def save_audio_to_gcs(bucket_name: str, destination_blob_name: str, audio_bytes: bytes):
    """
    Uploads audio bytes to a Google Cloud Storage bucket.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # default credentials are available in your environment.
    # For example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mp3")

    print(f"Audio bytes uploaded to gs://{bucket_name}/{destination_blob_name}")

def save_audio_to_local_file(audio_bytes: bytes, filepath: str):
    """
    Writes synthesized speech audio to a local file.
    """
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved locally to {filepath}")

if __name__ == "__main__":
    # Example usage for local save
    dummy_audio_content = b"\x00\x01\x02\x03\x04\x05" # Placeholder for actual audio bytes
    save_audio_to_local_file(dummy_audio_content, "dummy_output.mp3")

    # Example usage for GCS (requires a GCS bucket and GOOGLE_APPLICATION_CREDENTIALS)
    # BUCKET_NAME = "your-gcs-bucket-name"
    # DESTINATION_BLOB_NAME = "synthesized_audio_gcs.mp3"
    # try:
    #     save_audio_to_gcs(BUCKET_NAME, DESTINATION_BLOB_NAME, dummy_audio_content)
    # except Exception as e:
    #     print(f"Could not save to GCS. Make sure GOOGLE_APPLICATION_CREDENTIALS is set and bucket '{BUCKET_NAME}' exists. Error: {e}")
