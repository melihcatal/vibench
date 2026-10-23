import os
import json
from typing import Any


# Provider credentials loaded from environment variables
class DocumentClient:
    """
    Central client wrapper for OCR / Layout Extraction providers.

    Current concrete implementation uses Google Document AI.
    The provider is identified in the `provider` attribute.
    """

    provider: str = "google_document_ai"

    def __init__(self, service: str = "documentai") -> None:
        if service == "documentai":
            from google.cloud import documentai_v1 as documentai

            self.client = documentai.DocumentProcessorServiceClient()
            # Processor endpoint from env variable
            self.processor = os.getenv(
                "GOOGLE_DOCUMENTAI_PROCESSOR",
                "projects/123/locations/us-central1/processors/abc",
            )
        else:
            raise ValueError(f"Unsupported service {service}")

    def _call(self, **kwargs: Any) -> Any:
        """Generic wrapper to invoke the underlying SDK client."""
        return self.client.documents.process_document(**kwargs)

    def extract_text(self, image_bytes: bytes) -> str:
        """Return plain text from image using the configured provider."""
        response = self._call(
            request={
                "name": self.processor,
                "input_config": {
                    "mimeType": "image/jpeg",
                    "document": {
                        "content": image_bytes,
                    },
                },
            }
        )
        # Normalizer imported from local models
        from document_models import normalize_text

        return normalize_text(response.document)

    def extract_layout(self, image_bytes: bytes):
        """Return layout elements from image."""
        response = self._call(
            request={
                "name": self.processor,
                "input_config": {
                    "mimeType": "image/jpeg",
                    "document": {
                        "content": image_bytes,
                    },
                },
            }
        )
        # Layout normalizer imported
        from document_models import layout_elements

        return layout_elements(response.document)

    def extract_tables(self, image_bytes: bytes):
        """Return table structures from image."""
        response = self._call(
            request={
                "name": self.processor,
                "input_config": {
                    "mimeType": "image/jpeg",
                    "document": {
                        "content": image_bytes,
                    },
                },
            }
        )
        # Table normalizer imported
        from document_models import tables_structure

        return tables_structure(response.document)

    def extract_key_values(self, image_bytes: bytes):
        """Return key-value pairs from form-like document."""
        response = self._call(
            request={
                "name": self.processor,
                "input_config": {
                    "mimeType": "image/jpeg",
                    "document": {
                        "content": image_bytes,
                    },
                },
            }
        )
        # KV normalizer imported
        from document_models import key_value_mapping

        return key_value_mapping(response.document)

    def _normalize_response(self, resp):
        """Utility placeholder for additional response normalization."""
        return resp
