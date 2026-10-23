from typing import Dict, Any, List
from document_client import process_document
from document_models import DocumentField


def extract_invoice_fields(file_path: str) -> Dict[str, DocumentField]:
    """Extract vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI."""
    document = process_document(file_path)
    fields: Dict[str, DocumentField] = {}

    for entity in document.entities:
        field_name = entity.type_.lower()
        if field_name in ["vendor_name", "supplier_name"]:
            fields["vendor"] = {
                "field_name": "vendor",
                "value": entity.mention_text,
                "confidence": entity.confidence,
            }
        elif field_name == "transaction_date":
            fields["date"] = {
                "field_name": "date",
                "value": entity.normalized_value.text,
                "confidence": entity.confidence,
            }
        elif field_name == "total_amount":
            fields["total"] = {
                "field_name": "total",
                "value": entity.normalized_value.text,
                "confidence": entity.confidence,
            }

    line_items = []
    for page in document.pages:
        for table in page.tables:
            for row in table.header_rows + table.body_rows:
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
                        if "description" in text.lower():
                            item["description"] = text
                        elif "quantity" in text.lower():
                            item["quantity"] = text
                        elif "unit price" in text.lower():
                            item["unit_price"] = text
                        elif "amount" in text.lower():
                            item["amount"] = text
                if item:
                    line_items.append(item)

    if line_items:
        fields["line_items"] = {
            "field_name": "line_items",
            "value": line_items,
            "confidence": min(
                [entity.confidence for entity in document.entities], default=0.0
            ),
        }

    return fields
