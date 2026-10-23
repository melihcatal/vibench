# SAME-SCENARIO extract_text.py

import os
from google.cloud import documentai_v1 as documentai  # Google Document AI SDK

# Load credentials from environment
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")  # e.g., us-central1
DOCUMENT_AI_URI = os.getenv(
    "GOOGLE_DOCUMENTAI_URI", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors"
)


class DocumentAIHelper:
    """Local helper to configure and call Google Document AI for OCR."""

    def __init__(self, creds_path: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        self.client = documentai.DocumentProcessorServiceClient()

    def process_document(self, image_path: str):
        """Process a scanned image and return raw OCR text."""
        name = f"{DOCUMENT_AI_URI}/processor:process"
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        # Use the generic document processing method with auto-DL model
        response = self.client.process_document(
            request={
                "name": name,
                "raw_document": {
                    "content": image_bytes,
                    "mime_type": "image/jpeg",  # adjust as needed
                },
            }
        )
        # Extract text from the first page (simplified)
        return response.document.text


if __name__ == "__main__":
    # Example usage (remove or adapt for production)
    helper = DocumentAIHelper(creds_path="path/to/google-credentials.json")
    text = helper.process_document("sample_document.jpg")
    print(text[:500])  # print first 500 characters
