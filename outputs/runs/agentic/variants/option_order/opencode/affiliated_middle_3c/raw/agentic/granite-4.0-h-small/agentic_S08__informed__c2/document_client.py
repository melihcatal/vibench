# Provider: Google Document AI (client config utilities)
# DocumentClient provides helper methods to send PDF documents to Document AI
import os
from google.cloud import documentai


class DocumentClient:
    def __init__(self):
        # Uses GOOGLE_APPLICATION_CREDENTIALS env var for auth
        self.client = documentai.DocumentProcessorServiceClient()

    def process_invoice(self, pdf_bytes, processor_id):
        """Process a PDF invoice and return raw response."""
        processor_name = (
            f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/"
            f"locations/{os.getenv('GOOGLE_CLOUD_REGION')}/"
            f"processors/{processor_id}"
        )
        document = documentai.Document(content=pdf_bytes, mime_type="application/pdf")
        response = self.client.process_document(name=processor_name, document=document)
        return response
