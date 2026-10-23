# LATER-STEP document_field_extraction.py

import os
from google.cloud import documentai_v1 as documentai
from .document_client import OCRClient
from .document_models import normalize_response

# Load environment settings
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
DOCUMENT_AI_URI = os.getenv(
    "GOOGLE_DOCUMENTAI_URI", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors"
)


class FieldExtractor:
    """Extract structured fields (e.g., name, date, total) from OCR-normalized text using Document AI custom processors."""

    def __init__(self):
        self.client = OCRClient()
        self.processor_id = os.getenv("DOCUMENT_AI_FIELD_PROCESSOR_ID")
        if not self.processor_id:
            raise RuntimeError("DOCUMENT_AI_FIELD_PROCESSOR_ID not configured")

    def extract(self, image_path: str) -> dict:
        """Return a dict of extracted field names/values."""
        # First run OCR/layout detection (using our helper)
        raw = self.client.process(image_path)
        # Normalize response to our internal model
        normalized = normalize_response("google_documentai", raw)
        # NOTE: In practice you would call the *Custom* Document AI processor here.
        # For illustration we simulate extraction with a simple keyword search.
        extracted = self._simple_keyword_extraction(normalized)
        return extracted

    def _simple_keyword_extraction(self, normalized: dict) -> dict:
        text = normalized.get("text", "")
        fields = {}
        for kw, label in (
            ("total", "Total"),
            ("date", "Date"),
            ("invoice_number", "Invoice No."),
            ("vendor", "Vendor"),
        ):
            idx = text.lower().find(kw.lower())
            if idx != -1:
                # Grab a short substring after the keyword
                start = max(idx + len(kw), 0)
                snippet = text[start : start + 30].strip()
                fields[label] = snippet
        return fields


if __name__ == "__main__":
    extractor = FieldExtractor()
    fields = extractor.extract("sample_invoice.jpg")
    print("Extracted fields:", fields)
