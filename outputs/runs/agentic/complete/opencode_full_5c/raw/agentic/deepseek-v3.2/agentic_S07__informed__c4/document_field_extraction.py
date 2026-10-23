import os
from typing import Dict, List, Any, Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import (
    TextExtractionResponse,
    KeyValuePair,
    KeyValueExtractionResponse,
)


class DocumentFieldExtractor:
    """Extract structured fields from OCR-normalized document text using Azure Document Intelligence prebuilt invoice."""

    def __init__(self):
        endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not endpoint or not key:
            raise ValueError("Azure Document Intelligence credentials not configured")

        self.client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

    def extract_invoice_fields(
        self, image_path: str, mime_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured invoice fields using Azure Document Intelligence prebuilt invoice model.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, "rb") as f:
            image_content = f.read()

        poller = self.client.begin_analyze_document(
            model_id="prebuilt-invoice",
            document=image_content,
            content_type=mime_type or "image/jpeg",
        )

        result = poller.result()

        extracted_fields = {}

        for document in result.documents:
            fields = document.fields

            for field_name, field_value in fields.items():
                if field_value:
                    extracted_fields[field_name] = {
                        "value": field_value.content,
                        "confidence": field_value.confidence,
                        "bounding_regions": [
                            {
                                "page_number": region.page_number,
                                "polygon": [
                                    (point.x, point.y) for point in region.polygon
                                ],
                            }
                            for region in field_value.bounding_regions
                        ]
                        if hasattr(field_value, "bounding_regions")
                        else [],
                    }

        return {
            "fields": extracted_fields,
            "raw_response": result.to_dict(),
            "provider": "azure_document_intelligence_invoice",
        }

    def extract_fields_from_ocr(
        self,
        extraction_response: TextExtractionResponse,
        document_type: str = "invoice",
    ) -> KeyValueExtractionResponse:
        """
        Extract structured fields from OCR text by re-processing with specialized model.
        Note: This requires the original image, not just the text.
        """
        raise NotImplementedError(
            "Field extraction requires original image, not just OCR text"
        )

    def extract_receipt_fields(
        self, image_path: str, mime_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured receipt fields using Azure Document Intelligence prebuilt receipt model.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        with open(image_path, "rb") as f:
            image_content = f.read()

        poller = self.client.begin_analyze_document(
            model_id="prebuilt-receipt",
            document=image_content,
            content_type=mime_type or "image/jpeg",
        )

        result = poller.result()

        extracted_fields = {}

        for document in result.documents:
            fields = document.fields

            for field_name, field_value in fields.items():
                if field_value:
                    extracted_fields[field_name] = {
                        "value": field_value.content,
                        "confidence": field_value.confidence,
                    }

        return {
            "fields": extracted_fields,
            "raw_response": result.to_dict(),
            "provider": "azure_document_intelligence_receipt",
        }
