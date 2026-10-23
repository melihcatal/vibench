import os
from typing import Dict, Any
from document_client import get_di_client
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentBytesSource
from document_models import ExtractedField, LineItem, ReceiptExtract

def extract_receipt_fields(image_path: str) -> ReceiptExtract:
    client = get_di_client()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    analyze_request = AnalyzeDocumentRequest(bytes_source=DocumentBytesSource(image_bytes))
    poller = client.begin_analyze_document(model_id="prebuilt-receipt", analyze_request=analyze_request)
    result = poller.result()
    fields = result.fields
    merchant_field = fields.get('MerchantName')
    merchant = ExtractedField(content=merchant_field.content if merchant_field else '', confidence=merchant_field.confidence if merchant_field else 0.0)
    date_field = fields.get('TransactionDate')
    date = ExtractedField(content=date_field.content if date_field else '', confidence=date_field.confidence if date_field else 0.0)
    tax_field = fields.get('TotalSalesTax')
    tax = ExtractedField(content=tax_field.content if tax_field else '', confidence=tax_field.confidence if tax_field else 0.0) if tax_field else None
    total_field = fields.get('Total')
    total = ExtractedField(content=total_field.content if total_field else '', confidence=total_field.confidence if total_field else 0.0)
    items: list[LineItem] = []
    items_field = fields.get('Items')
    if items_field and items_field.values:
        for item_value in items_field.values:
            item_fields = item_value.fields
            desc_field = item_fields.get('Description') or item_fields.get('Item')
            qty_field = item_fields.get('Quantity')
            price_field = item_fields.get('Price')
            amt_field = item_fields.get('LineTotal')
            items.append(LineItem(
                description=desc_field.content if desc_field else '',
                quantity=float(qty_field.content) if qty_field else None,
                price=float(price_field.content) if price_field else None,
                amount=float(amt_field.content) if amt_field else 0.0
            ))
    return ReceiptExtract(merchant=merchant, date=date, tax=tax, total=total, items=items)
