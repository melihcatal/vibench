from google.cloud import storage
import os

class MessageAuditStore:
    def __init__(self, bucket_name=None):
        self.client = storage.Client()
        self.bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        if not self.bucket_name:
            raise ValueError("Google Cloud Storage bucket name must be provided or set as GCS_BUCKET_NAME environment variable.")
        self.bucket = self.client.bucket(self.bucket_name)

    def persist_message(self, record_id: str, message_content: str):
        """
        Persists a message record to Google Cloud Storage.
        """
        blob = self.bucket.blob(f"message_records/{record_id}.txt")
        blob.upload_from_string(message_content)
        print(f"Message record {record_id} persisted to gs://{self.bucket_name}/message_records/{record_id}.txt")

