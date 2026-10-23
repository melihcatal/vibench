# extract_key_values.py
# SAME-SCENARIO implementation file

# Using Google Document AI for form/key-value extraction
import io
from document_client import KeyValueExtractionClient

# Google Document AI client library
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import Document, DocumentPage


class GoogleFormExtractionClient(KeyValueExtractionClient):
    def __init__(
        self,
        project_id="your-gcp-project",
        location="us-central1",
        processor_id="your-form-processor-id",
    ):
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_id = (
            f"projects/{project_id}/locations/{location}/processors/{processor_id}"
        )

    def extract(self, document_bytes):
        # Send document to processor
        response = self.client.process_document(
            parent=self.processor_id,
            document=Document(content=document_bytes, mime_type="application/pdf"),
        )
        # Normalize key-value pairs
        kv_pairs = {}
        for page in response.document.pages:
            for entity in page.entities:
                if "key" in entity.type_:
                    key = entity.type_.replace("key", "").strip()
                    value = next(
                        (e for e in page.entities if e.parent_id == entity.id), None
                    )
                    kv_pairs[key] = value.text if value else ""
        return kv_pairs


# Example usage (not executed here)
# client = GoogleFormExtractionClient()
# data = client.extract(open('invoice.pdf', 'rb').read())
# print(data)
