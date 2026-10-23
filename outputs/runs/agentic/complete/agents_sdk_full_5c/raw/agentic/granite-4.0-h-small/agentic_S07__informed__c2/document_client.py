import os
from typing import Optional
import google.cloud.documentai as ga_documentai

# Service identifier:
# Provider: Google Document AI (OCR client utility)

INSTANCE_ID = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # service account JSON path
OCR_PROCESSOR_ID = os.getenv('OCR_PROCESSOR_ID', 'projects/<PROJECT>/locations/us-central1/processors/<PROCESSOR>')

class DocumentOcrClient:
    def __init__(self):
        self._credentials = ga_documentai.Credentials.from_service_account_file(INSTANCE_ID)
        self._client = ga_documentai.DocumentProcessorServiceClient(credentials=self._credentials)

    def extract_text(self, image_bytes: bytes) -> str:
        document = ga_documentai.Document.fromJson({"content": image_bytes, "mime_type": "image/jpeg"})
        response = self._client.process_document(name=OCR_PROCESSOR_ID, raw_document=document)
        return response.document.text
