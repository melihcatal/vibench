import os
import time
from typing import Dict, Any
from document_client import get_di_client
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentBytesSource
from document_models import ExtractedField, LineItem, InvoiceExtract

def extract_invoice_fields(image_path: str) -> InvoiceExtract:
    client = get_di_client()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    analyze_request = AnalyzeDocumentRequest(bytes_source=DocumentBytesSource(image_bytes))
    poller = client.begin_analyze_document(model_id="prebuilt-invoice", analyze_request=analyze_request)
    result = poller.result()
    fields = result.fields
    vendor_field = fields.get('VendorName') or fields.get('SupplierName')
    vendor = ExtractedField(content=vendor_field.content if vendor_field else '', confidence=vendor_field.confidence if vendor_field else 0.0)
    date_field = fields.get('InvoiceDate')
    date = ExtractedField(content=date_field.content if date_field else '', confidence=date_field.confidence if date_field else 0.0)
    total_field = fields.get('AmountDue') or fields.get('InvoiceTotal')
    total = ExtractedField(content=total_field.content if total_field else '', confidence=total_field.confidence if total_field else 0.0)
    line_items: list[LineItem] = []
    items_field = fields.get('Items')
    if items_field and items_field.values:
        for item_value in items_field.values:
            item_fields = item_value.fields
            desc_field = item_fields.get('Description')
            qty_field = item_fields.get('Quantity')
            price_field = item_fields.get('UnitPrice')
            amt_field = item_fields.get('Amount') or item_fields.get('LineTotal')
            line_items.append(LineItem(
                description=desc_field.content if desc_field else '',
                quantity=float(qty_field.content) if qty_field else None,
                price=float(price_field.content) if price_field else None,
                amount=float(amt_field.content) if amt_field else 0.0
            ))
    return InvoiceExtract(vendor=vendor, date=date, total=total, line_items=line_items)
