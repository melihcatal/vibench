import os
from typing import Literal


class DocumentClient:
    """Local helper providing a unified interface to external OCR/layout providers."""

    def __init__(
        self,
        service: Literal[
            "azure_ocr", "aws_textract", "google_document_ai", "azure_form_recognizer"
        ],
    ):
        self.service = service
        # Load credentials/environment variables for the chosen provider.
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> dict:
        """Retrieve provider-specific credentials from environment variables."""
        if self.service == "azure_ocr":
            return {
                "endpoint": os.getenv("AZURE_VISION_ENDPOINT"),
                "key": os.getenv("AZURE_VISION_KEY"),
            }
        elif self.service == "aws_textract":
            return {"region_name": os.getenv("AWS_REGION")}
        elif self.service == "google_document_ai":
            return {
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "location": os.getenv("GOOGLE_LOCATION"),
                "processor_id": os.getenv("GOOGLE_DOCUMENT_AI_ID"),
            }
        elif self.service == "azure_form_recognizer":
            return {
                "endpoint": os.getenv("AZURE_FORM_ENDPOINT"),
                "key": os.getenv("AZURE_FORM_KEY"),
            }
        else:
            raise ValueError(f"Unsupported OCR service: {self.service}")

    def ocr_image(self, image_bytes: bytes) -> dict:
        """Delegate to provider's image OCR endpoint."""
        if self.service == "azure_ocr":
            return self._azure_ocr(image_bytes)
        elif self.service == "aws_textract":
            return self._aws_textract(image_bytes)
        elif self.service == "google_document_ai":
            return self._google_document_ai(image_bytes)
        elif self.service == "azure_form_recognizer":
            return self._azure_form_recognizer(image_bytes)
        else:
            raise RuntimeError("Invalid OCR service in DocumentClient")

    def extract_tables(self, image_bytes: bytes) -> list[dict]:
        """Provider‑specific table extraction."""
        if self.service == "google_document_ai":
            return self._google_extract_tables(image_bytes)
        else:
            raise NotImplementedError(
                f"Table extraction not implemented for {self.service}"
            )

    def extract_key_values(self, image_bytes: bytes) -> list[dict]:
        """Provider‑specific key‑value extraction."""
        if self.service == "azure_form_recognizer":
            return self._azure_form_key_values(image_bytes)
        else:
            raise NotImplementedError(
                f"Key‑value extraction not implemented for {self.service}"
            )

    # ------------------------------------------------------------------
    # Provider‑specific helper methods (stubbed for illustration)
    # ------------------------------------------------------------------
    def _azure_ocr(self, image_bytes: bytes) -> dict:
        # Placeholder: call Azure Computer Vision OCR API
        return {"text": "sample text"}

    def _aws_textract(self, image_bytes: bytes) -> dict:
        # Placeholder: call AWS Textract API
        return {"blocks": []}

    def _google_document_ai(self, image_bytes: bytes) -> dict:
        # Placeholder: call Google Document AI API
        return {"text": "sample structured text"}

    def _azure_form_recognizer(self, image_bytes: bytes) -> list[dict]:
        # Placeholder: call Azure Form Recognizer API
        return [{"key": "Field1", "value": "Sample value"}]

    def _google_extract_tables(self, image_bytes: bytes) -> list[dict]:
        # Placeholder: call Google Document AI table extraction
        return [{"rows": [], "columns": []}]
