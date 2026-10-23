import boto3
import os
from typing import Dict, Any
from document_client import get_textract_client
from document_models import ExtractedField, LineItem, DocumentExtractionResponse

def extract_receipt_fields(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = get_textract_client(config.get("region"))
    response = client.analyze_expense(Document={"Bytes": payload["document_bytes"]})
    
    receipts = []
    for document in response["ExpenseDocuments"]:
        fields = {f["Type"]["Text"]: f["ValueDetection"] for f in document["SummaryFields"]}
        
        merchant_field = fields.get("MERCHANT_NAME")
        total_field = fields.get("TOTAL")
        tax_field = fields.get("TAX")
        date_field = fields.get("INVOICE_RECEIPT_DATE")

        merchant = ExtractedField(value=merchant_field.get("Text") if merchant_field else None, confidence=merchant_field.get("Confidence") if merchant_field else None)
        total = ExtractedField(value=total_field.get("Text") if total_field else None, confidence=total_field.get("Confidence") if total_field else None)
        tax = ExtractedField(value=tax_field.get("Text") if tax_field else None, confidence=tax_field.get("Confidence") if tax_field else None)
        date = ExtractedField(value=date_field.get("Text") if date_field else None, confidence=date_field.get("Confidence") if date_field else None)

        items = []
        for group in document.get("LineItemGroups", []):
            for item in group["LineItems"]:
                values = {f["Type"]["Text"]: f["ValueDetection"].get("Text", "") for f in item["LineItemExpenseFields"]}
                items.append(LineItem(description=values.get("ITEM"), quantity=values.get("QUANTITY"), amount=values.get("PRICE")))

        receipts.append(DocumentExtractionResponse(merchant=merchant, total=total, tax=tax, date=date, line_items=items).model_dump())
        
    return {"receipts": receipts}
