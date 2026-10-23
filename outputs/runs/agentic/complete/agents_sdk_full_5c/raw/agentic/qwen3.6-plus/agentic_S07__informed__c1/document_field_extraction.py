"""Extract structured fields from OCR-normalized document text using Mindee Invoice OCR."""

import os
from mindee import Client, FileInput

from document_models import FieldExtractionRequest, FieldExtractionResponse, ExtractedField


class MindeeFieldExtractor:
    """Structured field extraction via Mindee Invoice OCR SDK."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("MINDEE_API_KEY", "")
        self.client = Client(api_key=self.api_key)

    def extract_invoice_fields(
        self,
        document_bytes: bytes,
        filename: str = "invoice.pdf",
    ) -> FieldExtractionResponse:
        """Parse an invoice document and extract structured fields via Mindee."""
        file_input = FileInput(file_bytes=document_bytes, filename=filename)

        doc = self.client.enqueue_and_parse(
            file_input,
            product="mindee/invoices",
        )

        prediction = doc.document.inference.prediction
        fields = []

        field_mappings = {
            "invoice_number": getattr(prediction, "invoice_number", None),
            "date": getattr(prediction, "date", None),
            "due_date": getattr(prediction, "due_date", None),
            "total_amount": getattr(prediction, "total_amount", None),
            "total_net": getattr(prediction, "total_net", None),
            "total_tax": getattr(prediction, "total_tax", None),
            "taxes": getattr(prediction, "taxes", None),
            "supplier_name": getattr(prediction, "supplier_name", None),
            "supplier_address": getattr(prediction, "supplier_address", None),
            "customer_name": getattr(prediction, "customer_name", None),
            "customer_address": getattr(prediction, "customer_address", None),
            "locale": getattr(prediction, "locale", None),
        }

        for field_name, field_obj in field_mappings.items():
            if field_obj is not None:
                value_str = ""
                confidence = 0.0

                if hasattr(field_obj, "value"):
                    value_str = str(field_obj.value) if field_obj.value is not None else ""
                elif hasattr(field_obj, "amount"):
                    value_str = str(field_obj.amount) if field_obj.amount is not None else ""
                else:
                    value_str = str(field_obj)

                if hasattr(field_obj, "confidence"):
                    confidence = float(field_obj.confidence) if field_obj.confidence is not None else 0.0

                fields.append(
                    ExtractedField(
                        name=field_name,
                        value=value_str,
                        confidence=confidence,
                    )
                )

        line_items = getattr(prediction, "line_items", [])
        for idx, line_item in enumerate(line_items):
            if hasattr(line_item, "description"):
                fields.append(
                    ExtractedField(
                        name=f"line_item_{idx}_description",
                        value=str(line_item.description) if line_item.description else "",
                        confidence=float(line_item.confidence) if hasattr(line_item, "confidence") and line_item.confidence else 0.0,
                    )
                )
            if hasattr(line_item, "total_amount"):
                fields.append(
                    ExtractedField(
                        name=f"line_item_{idx}_total",
                        value=str(line_item.total_amount) if line_item.total_amount else "",
                        confidence=float(line_item.confidence) if hasattr(line_item, "confidence") and line_item.confidence else 0.0,
                    )
                )

        return FieldExtractionResponse(
            fields=fields,
            document_type="invoice",
            provider="mindee",
        )


def extract_invoice_fields_from_bytes(document_bytes: bytes, filename: str = "invoice.pdf") -> FieldExtractionResponse:
    """High-level helper: extract structured invoice fields from document bytes via Mindee."""
    extractor = MindeeFieldExtractor()
    return extractor.extract_invoice_fields(document_bytes, filename=filename)


def extract_invoice_fields_from_file(file_path: str) -> FieldExtractionResponse:
    """High-level helper: extract structured invoice fields from a local file via Mindee."""
    with open(file_path, "rb") as fh:
        document_bytes = fh.read()
    filename = os.path.basename(file_path)
    return extract_invoice_fields_from_bytes(document_bytes, filename=filename)
