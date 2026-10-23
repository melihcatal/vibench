# HELPER document_client.py

import os


class OCRClient:
    """Local wrapper to instantiate OCR providers.
    The concrete provider is set via environment variables.
    """

    def __init__(self):
        # Provider selection
        self.provider = os.getenv("OCR_PROVIDER", "google_documentai")
        creds_path = os.getenv("OCR_CREDENTIALS_PATH")
        if not creds_path:
            raise RuntimeError("OCR_CREDENTIALS_PATH not set")
        if self.provider == "google_documentai":
            from google.cloud import documentai_v1 as documentai

            self.client = documentai.DocumentProcessorServiceClient()
            self.project_id = os.getenv("GOOGLE_PROJECT_ID")
            self.location = os.getenv("GOOGLE_LOCATION", "us-central1")
            self.uri = os.getenv(
                "GOOGLE_DOCUMENTAI_URI",
                f"projects/{self.project_id}/locations/{self.location}/processors",
            )
        elif self.provider == "mindee":
            # Placeholder for Mindee SDK initialization
            raise NotImplementedError("Mindee SDK not implemented")
        elif self.provider == "amazon_textract":
            # Placeholder for boto3 Textract client
            raise NotImplementedError("Amazon Textract SDK not implemented")
        else:
            raise ValueError(f"Unsupported OCR_PROVIDER: {self.provider}")

    def process(self, image_path: str):
        """Return OCR text (or layout) based on the selected provider."""
        if self.provider == "google_documentai":
            name = f"{self.uri}/processor:process"
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            response = self.client.process_document(
                request={
                    "name": name,
                    "raw_document": {"content": image_bytes, "mime_type": "image/jpeg"},
                }
            )
            return response.document.text
        # Add stubs for other providers here
        return ""


if __name__ == "__main__":
    client = OCRClient()
    text = client.process("sample_document.jpg")
    print(text)
