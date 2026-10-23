import os
from document_client import read_pdf_bytes, validate_env
from document_models import InvoiceExtract, ExtractedField, LineItem
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import List

validate_env("azure_di")


def extract_invoice_fields(invoice_path: str) -> InvoiceExtract:
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    pdf_bytes = read_pdf_bytes(invoice_path)
    poller = client.begin_analyze_document(
        "prebuilt-invoice", document=pdf_bytes, content_type="application/pdf"
    )
    result: AnalyzeResult = poller.result()
    doc = result.documents[0]
    vendor_field = doc.fields.get("VendorName")
    vendor = ExtractedField(
        value=vendor_field.content if vendor_field else "",
        confidence=vendor_field.confidence if vendor_field else 0.0,
    )
    date_field = doc.fields.get("InvoiceDate")
    date = ExtractedField(
        value=date_field.content if date_field else "",
        confidence=date_field.confidence if date_field else 0.0,
    )
    total_field = doc.fields.get("InvoiceTotal") or doc.fields.get("AmountDue")
    total = ExtractedField(
        value=total_field.content if total_field else "",
        confidence=total_field.confidence if total_field else 0.0,
    )
    line_items: List[LineItem] = []
    line_field = doc.fields.get("LineItems")
    if line_field and line_field.value:
        for item_value in line_field.value:
            item_fields = item_value.fields
            desc_field = item_fields.get("Description")
            desc = desc_field.content if desc_field else ""
            desc_conf = desc_field.confidence if desc_field else 0.0
            qty_field = item_fields.get("Quantity")
            qty = float(qty_field.content) if qty_field and qty_field.content else None
            qty_conf = qty_field.confidence if qty_field else 0.0
            unit_field = item_fields.get("UnitPrice")
            unit_price = (
                float(unit_field.content) if unit_field and unit_field.content else None
            )
            unit_conf = unit_field.confidence if unit_field else 0.0
            amount_field = item_fields.get("Amount")
            amount = (
                float(amount_field.content)
                if amount_field and amount_field.content
                else None
            )
            amount_conf = amount_field.confidence if amount_field else 0.0
            conf = (desc_conf + qty_conf + unit_conf + amount_conf) / 4.0
            line_items.append(
                LineItem(
                    description=desc,
                    quantity=qty,
                    unit_price=unit_price,
                    total=amount,
                    confidence=conf,
                )
            )
    return InvoiceExtract(vendor=vendor, date=date, total=total, line_items=line_items)
