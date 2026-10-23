import os
from document_client import read_pdf_bytes, validate_env
from document_models import ReceiptExtract, ExtractedField, LineItem
from mindee import Client, product

validate_env("mindee")


def extract_receipt_fields(receipt_path: str) -> ReceiptExtract:
    mindee_client = Client(api_key=os.getenv("MINDEE_API_KEY"))
    pdf_bytes = read_pdf_bytes(receipt_path)
    result = mindee_client.load_document(product.Receipt_v4, pdf_bytes)
    doc_pred = result.document.inference.prediction
    merchant = ExtractedField(
        value=doc_pred.merchant.name or "",
        confidence=getattr(doc_pred.merchant, "confidence", 0.0),
    )
    date = ExtractedField(
        value=doc_pred.date.value if doc_pred.date else "",
        confidence=getattr(doc_pred.date, "confidence", 0.0),
    )
    tax_val = sum([t.value for t in doc_pred.taxes]) if doc_pred.taxes else 0.0
    tax_confs = [t.confidence for t in doc_pred.taxes] if doc_pred.taxes else []
    tax_conf = sum(tax_confs) / len(tax_confs) if tax_confs else 0.0
    tax = ExtractedField(value=str(tax_val), confidence=tax_conf)
    total_val = getattr(doc_pred.total_amount, "value", 0.0)
    total_conf = getattr(doc_pred.total_amount, "confidence", 0.0)
    total = ExtractedField(value=str(total_val), confidence=total_conf)
    line_items = []
    for supply in doc_pred.supplies or []:
        line_items.append(
            LineItem(
                description=getattr(supply, "description", ""),
                quantity=getattr(supply, "quantity", None),
                unit_price=getattr(supply, "unit_price", None),
                total=getattr(supply.total_amount, "value", None),
                confidence=getattr(supply, "confidence", 0.0),
            )
        )
    return ReceiptExtract(
        merchant=merchant, date=date, tax=tax, total=total, line_items=line_items
    )
