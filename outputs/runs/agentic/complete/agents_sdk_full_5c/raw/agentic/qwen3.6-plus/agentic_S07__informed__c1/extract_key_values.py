"""Extract key-value pairs from a form-like document using Mindee Document OCR API."""

import os
from mindee import Client, PredictResponse, FileInput
from mindee.product.fr import CarteVitaleV1
from mindee.product.us import BankCheckV1

from document_models import KeyValueRequest, KeyValueResponse, KeyValuePair


class MindeeKeyValueExtractor:
    """Form key-value extraction via the Mindee Document OCR SDK."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("MINDEE_API_KEY", "")
        self.client = Client(api_key=self.api_key)

    def extract_key_values(
        self,
        document_bytes: bytes,
        filename: str = "document.pdf",
    ) -> KeyValueResponse:
        """Send document to Mindee and extract form key-value pairs."""
        file_input = FileInput(file_bytes=document_bytes, filename=filename)

        doc = self.client.enqueue_and_parse(
            file_input,
            product="mindee/custom_v1",
        )

        pairs = []
        fields = doc.document.inference.prediction.fields or {}

        for field_name, field_value in fields.items():
            if field_value is not None:
                kv = KeyValuePair(
                    key=field_name,
                    value=str(field_value) if not isinstance(field_value, dict) else str(field_value),
                    confidence=getattr(field_value, "confidence", None),
                )
                pairs.append(kv)

        pages = doc.document.inference.pages or []
        for page in pages:
            page_fields = page.prediction.fields or {}
            for field_name, field_value in page_fields.items():
                if field_value is not None:
                    kv = KeyValuePair(
                        key=field_name,
                        value=str(field_value) if not isinstance(field_value, dict) else str(field_value),
                        confidence=getattr(field_value, "confidence", None),
                        page_number=page.page_id,
                    )
                    pairs.append(kv)

        return KeyValueResponse(
            key_value_pairs=pairs,
            page_count=len(pages) if pages else 1,
            provider="mindee",
        )


def extract_key_values_from_bytes(document_bytes: bytes, filename: str = "document.pdf") -> KeyValueResponse:
    """High-level helper: extract key-value pairs from document bytes via Mindee."""
    extractor = MindeeKeyValueExtractor()
    return extractor.extract_key_values(document_bytes, filename=filename)


def extract_key_values_from_file(file_path: str) -> KeyValueResponse:
    """High-level helper: extract key-value pairs from a local file via Mindee."""
    with open(file_path, "rb") as fh:
        document_bytes = fh.read()
    filename = os.path.basename(file_path)
    return extract_key_values_from_bytes(document_bytes, filename=filename)
