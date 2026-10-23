from typing import Dict, Any, List
from google.cloud import storage
import json
import os

# Provider: Google Cloud Storage
# Model/Service: storage.Client
# Environment Variable: GOOGLE_APPLICATION_CREDENTIALS


class MessageSummaryStore:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def store_summary(self, message_id: str, summary_data: Dict[str, Any]) -> str:
        """
        Stores a message processing summary in Google Cloud Storage.
        Returns the blob name.
        """
        blob = self.bucket.blob(f"summaries/{message_id}.json")
        blob.upload_from_string(json.dumps(summary_data))
        return blob.name
