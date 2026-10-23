import os
import json
from google.cloud import storage


class DocumentClient:
    """Local configuration and client utilities for OCR and Layout Extraction."""

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor = os.getenv("DOCUMENTAI_PROCESSOR")
        # Generate a processor name like projects/PROJECT/locations/us-central1/processors/DOC_PROC
        self.processor_name = f"projects/{self.project_id}/locations/us-central1/processors/{self.processor}"
        self.storage_client = storage.Client(project=self.project_id)

    def preprocess_document(self, image_path):
        """Upload local image to GCS and prepare for processing."""
        bucket_name = os.getenv("GCS_BUCKET")
        blob_name = f"uploads/{os.path.basename(image_path)}"
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(image_path)
        return f"gs://{bucket_name}/{blob_name}"
