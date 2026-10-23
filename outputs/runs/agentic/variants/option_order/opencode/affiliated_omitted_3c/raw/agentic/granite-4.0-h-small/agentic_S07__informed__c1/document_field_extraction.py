# document_field_extraction.py
# LATER-STEP implementation file

# Using Google Document AI Invoice Parser for structured field extraction
import io
from document_client import KeyValueExtractionClient

# Google Document AI client library
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import Document, DocumentPage


class InvoiceFieldExtractor(KeyValueExtractionClient):
    def __init__(
        self,
        project_id="your-gcp-project",
        location="us-central1",
        processor_id="invoice-processor",
    ):
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_full_id = (
            f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        )

    def extract_fields(self, pdf_bytes: bytes) -> Dict[str, Any]:
        response = self.client.process_document(
            parent=self.processor_full_id,
            document=Document(content=pdf_bytes, mime_type="application/pdf"),
        )
        fields = {}
        for page in response.document.pages:
            for entity in page.entities:
                # Simple heuristic: key entities end with ':'
                if entity.type_.endswith(":"):
                    key = entity.type_.rstrip(":")
                    value = next(
                        (e for e in page.entities if e.parent_id == entity.id), None
                    )
                    fields[key] = value.text if value else ""
        return fields


# Usage example (not executed here)
# extractor = InvoiceFieldExtractor()
# pdf = open('invoice.pdf', 'rb').read()
# field_dict = extractor.extract_fields(pdf)
# print(field_dict)
