from typing import Dict, Any
from document_client import DocumentClient
from document_models import InvoiceFields, LineItem, parse_date


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    client = DocumentClient()
    document = client.process_document(file_path)

    invoice_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": [],
        "confidence": document.confidence,
    }

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            invoice_data["vendor"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice_data["date"] = parse_date(entity.mention_text)
        elif entity.type_ == "total_amount":
            invoice_data["total"] = float(entity.mention_text)
        elif entity.type_ == "line_item":
            line_item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item["description"] = prop.mention_text
                elif prop.type_ == "quantity":
                    line_item["quantity"] = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type_ == "unit_price":
                    line_item["unit_price"] = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
                elif prop.type_ == "amount":
                    line_item["amount"] = (
                        float(prop.mention_text) if prop.mention_text else None
                    )
            if line_item:
                invoice_data["line_items"].append(LineItem(**line_item))

    return InvoiceFields(**invoice_data).dict()
