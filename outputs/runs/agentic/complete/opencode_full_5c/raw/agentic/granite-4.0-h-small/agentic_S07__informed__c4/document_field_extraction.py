import os
from google.cloud import documentai
from document_models import DocumentRequest, ExtractedText, normalize_text

# Google Document AI configuration
PROJECT_ID = "your-project"
LOCATION = "us-central1"
PROCESSOR_ID = "your-processor-id"


class GoogleDocumentFieldExtractor:
    def __init__(self):
        # Load credentials from env
        self.client = documentai.DocumentProcessorServiceClient()

    def extract_structured_fields(self, request: DocumentRequest) -> Dict[str, Any]:
        """
        Extract structured fields from OCR-normalized document text.
        The method expects a DocumentRequest containing raw extracted text.
        For simplicity, we simulate field extraction using key-term search.
        In production you would integrate a classifier or schema-driven parser.
        """
        text: ExtractedText = normalize_text(request.to_dict())
        extracted = self._extract_fields_from_text(text.text)
        return extracted

    def _extract_fields_from_text(self, text: str) -> Dict[str, str]:
        """Dummy field extraction for illustration."""
        # Example heuristic: split on newlines and treat first word as key
        fields = {}
        for line in text.splitlines():
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                fields[key] = value
        return fields


def main():
    extractor = GoogleDocumentFieldExtractor()
    # Simulate a DocumentRequest that might come from an earlier step
    request = DocumentRequest(
        gcs_uri="gs://bucket/document.png",
        raw_response=True,
        metadata={"source": "Google Document AI"},
    )
    # Assume `extracted_text` is obtained from extract_text.py
    extracted_text = "Invoice Date: 2023-01-15\nTotal Amount: $1500.00"
    request_fields = extractor.extract_structured_fields(request)
    print("Extracted fields:", request_fields)


if __name__ == "__main__":
    main()
