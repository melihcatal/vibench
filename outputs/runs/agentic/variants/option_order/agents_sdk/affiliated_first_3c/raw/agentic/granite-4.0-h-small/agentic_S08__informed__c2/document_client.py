import os
from google.cloud import documentai_v1 as documentai

class DocumentClient:
    def __init__(self):
        # Uses the environment variable GOOGLE_APPLICATION_CREDENTIALS for auth
        self.client = documentai.DocumentProcessorServiceClient()
        # Optional: define processor ID and location once here for reuse
        self.processor_id = os.getenv("INVOICE_PROCESSOR_ID") or "INVOICE_PROCESSOR_ID"
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or "PROJECT_ID"
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    def process_document(self, raw_document, mime_type="application/pdf"):
        processor_name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
        response = self.client.process_document(name=processor_name, document=documentai.Document(raw_document=raw_document, mime_type=mime_type))
        return response
