from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from storage_client import get_storage_client
from typing import Optional
import os

class StoredDocumentOCR:
    def __init__(self):
        self.documentai_client = documentai.DocumentProcessorServiceClient()
        self.storage_client = get_storage_client()
        self.processor_name = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")
        if not self.processor_name:
            raise ValueError("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME must be set")

    def run_ocr(self, bucket_name: str, object_key: str) -> str:
        """Run OCR on a document stored in Google Cloud Storage using Google Document AI."""
        gcs_uri = f"gs://{bucket_name}/{object_key}"
        request = {
            "name": self.processor_name,
            "raw_document": {
                "gcs_document": {
                    "gcs_uri": gcs_uri,
                    "mime_type": self._detect_mime_type(bucket_name, object_key)
                }
            }
        }
        result = self.documentai_client.process_document(request=request)
        return result.document.text

    def _detect_mime_type(self, bucket_name: str, object_key: str) -> str:
        """Detect MIME type of a Google Cloud Storage object."""
        blob = self.storage_client.bucket(bucket_name).blob(object_key)
        blob.reload()
        return blob.content_type or "application/pdf"