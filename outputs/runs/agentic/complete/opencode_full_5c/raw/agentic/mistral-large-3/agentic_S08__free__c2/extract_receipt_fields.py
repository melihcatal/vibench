from typing import Dict, Any, List
from document_client import process_document
from document_models import DocumentField


def extract_receipt_fields(file_path: str) -> Dict[str, DocumentField]:
    """Extract merchant, tax, total, and items from a receipt using Google Cloud Document AI."""
    document = process_document(file_path)
    fields: Dict[str, DocumentField] = {}

    for entity in document.entities:
        field_name = entity.type_.lower()
        if field_name in ["merchant_name", "supplier_name"]:
            fields["merchant"] = {
                "field_name": "merchant",
                "value": entity.mention_text,
                "confidence": entity.confidence,
            }
        elif field_name == "tax_amount":
            fields["tax"] = {
                "field_name": "tax",
                "value": entity.normalized_value.text,
                "confidence": entity.confidence,
            }
        elif field_name == "total_amount":
            fields["total"] = {
                "field_name": "total",
                "value": entity.normalized_value.text,
                "confidence": entity.confidence,
            }
        elif field_name == "transaction_date":
            fields["date"] = {
                "field_name": "date",
                "value": entity.normalized_value.text,
                "confidence": entity.confidence,
            }

    items = []
    for page in document.pages:
        for table in page.tables:
            for row in table.body_rows:
                item = {}
                for cell in row.cells:
                    if cell.layout.text_anchor.text_segments:
                        text = "".join(
                            [
                                document.text[
                                    int(segment.start_index) : int(segment.end_index)
                                ]
                                for segment in cell.layout.text_anchor.text_segments
                            ]
                        )
                        if "description" in text.lower() or "item" in text.lower():
                            item["description"] = text
                        elif "price" in text.lower() or "amount" in text.lower():
                            item["amount"] = text
                if item:
                    items.append(item)

    if items:
        fields["items"] = {
            "field_name": "items",
            "value": items,
            "confidence": min(
                [entity.confidence for entity in document.entities], default=0.0
            ),
        }

    return fields
