import os
from typing import Optional
from google.cloud import documentai_v1 as documentai
from storage_client import IBMCloudStorageClient


class GoogleDocumentAIOCR:
    """
    Runs OCR on a document stored in IBM Cloud Object Storage using Google Document AI.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
        self.processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

        if not all([self.project_id, self.processor_id]):
            raise ValueError("Google Document AI credentials not configured.")

        self.client = documentai.DocumentProcessorServiceClient()
        self.storage_client = IBMCloudStorageClient()

    def process_document(
        self, bucket_name: str, object_key: str, mime_type: Optional[str] = None
    ) -> str:
        """
        Processes a document from IBM COS using Google Document AI OCR.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            mime_type: MIME type of the document.

        Returns:
            str: Extracted text from the document.
        """
        try:
            # Download the document from IBM COS
            response = self.storage_client.get_client().get_object(
                Bucket=bucket_name, Key=object_key
            )
            document_content = response["Body"].read()

            # Process the document using Google Document AI
            processor_name = self.client.processor_path(
                self.project_id, self.location, self.processor_id
            )

            document = {"content": document_content, "mime_type": mime_type}
            request = {"name": processor_name, "raw_document": document}
            result = self.client.process_document(request=request)

            return result.document.text
        except Exception as e:
            raise Exception(f"Failed to process document with OCR: {e}")
