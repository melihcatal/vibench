from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from typing import Dict, Any, Optional
import os

class InvoiceExtractor:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
        self.processor_id = os.getenv("GOOGLE_DOCUMENT_AI_INVOICE_PROCESSOR_ID")
        self.client = self._initialize_client()

    def _initialize_client(self) -> documentai.DocumentProcessorServiceClient:
        client_options = ClientOptions(api_endpoint=f"{self.location}-documentai.googleapis.com")
        return documentai.DocumentProcessorServiceClient(client_options=client_options)

    def extract_fields(self, file_path: str, mime_type: str = "application/pdf") -> Dict[str, Any]:
        with open(file_path, "rb") as file:
            document_content = file.read()

        name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
        request = {
            "name": name,
            "raw_document": {
                "content": document_content,
                "mime_type": mime_type
            }
        }

        result = self.client.process_document(request=request)
        document = result.document
        return self._parse_invoice_fields(document)

    def _parse_invoice_fields(self, document: documentai.Document) -> Dict[str, Any]:
        fields = {
            "vendor": self._get_field_text(document, "vendor_name"),
            "date": self._get_field_text(document, "invoice_date"),
            "total": self._get_field_text(document, "total_amount"),
            "line_items": self._get_line_items(document),
            "confidence": document.confidence
        }
        return fields

    def _get_field_text(self, document: documentai.Document, field_name: str) -> Optional[str]:
        for entity in document.entities:
            if entity.type_ == field_name:
                return entity.mention_text
        return None

    def _get_line_items(self, document: documentai.Document) -> list:
        line_items = []
        for entity in document.entities:
            if entity.type_ == "line_item" and entity.properties:
                line_item = {
                    "description": self._get_property_text(entity, "description"),
                    "quantity": self._get_property_text(entity, "quantity"),
                    "unit_price": self._get_property_text(entity, "unit_price"),
                    "amount": self._get_property_text(entity, "amount")
                }
                line_items.append(line_item)
        return line_items

    def _get_property_text(self, entity: documentai.Entity, property_name: str) -> Optional[str]:
        for prop in entity.properties:
            if prop.type_ == property_name:
                return prop.mention_text
        return None