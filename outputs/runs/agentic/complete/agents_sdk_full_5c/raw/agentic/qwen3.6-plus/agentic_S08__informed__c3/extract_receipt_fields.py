"""Extract merchant, tax, total, and items from a receipt using Azure Document Intelligence."""

import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import ReceiptExtractionResult, ReceiptItem
from document_client import get_document_intelligence_client


def extract_receipt_fields(document_path: str) -> ReceiptExtractionResult:
    """Extract structured fields from a receipt document.

    Uses Azure Document Intelligence prebuilt-receipt model (model ID: prebuilt-receipt).
    Returns merchant name, tax amount, total, and line items.
    """
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://<your-resource>.cognitiveservices.azure.com/"
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-receipt",
            body=f
        )
        result = poller.result()

    receipts = result.documents
    if not receipts:
        return ReceiptExtractionResult(
            merchant_name="",
            tax_amount=0.0,
            total_amount=0.0,
            items=[],
            confidence=0.0,
            raw_fields={}
        )

    receipt = receipts[0]
    fields = receipt.fields

    merchant_name = ""
    merchant_confidence = 0.0
    if "MerchantName" in fields:
        merchant_field = fields["MerchantName"]
        merchant_name = merchant_field.value or ""
        merchant_confidence = merchant_field.confidence or 0.0

    tax_amount = 0.0
    tax_confidence = 0.0
    if "TotalTax" in fields:
        tax_field = fields["TotalTax"]
        tax_amount = float(tax_field.value) if tax_field.value else 0.0
        tax_confidence = tax_field.confidence or 0.0

    total_amount = 0.0
    total_confidence = 0.0
    if "Total" in fields:
        total_field = fields["Total"]
        total_amount = float(total_field.value) if total_field.value else 0.0
        total_confidence = total_field.confidence or 0.0

    items = []
    items_confidence = 0.0
    if "Items" in fields:
        items_field = fields["Items"]
        if items_field.value:
            for idx, item in enumerate(items_field.value):
                description = ""
                quantity = 0.0
                price = 0.0
                total_price = 0.0

                if "Description" in item.value:
                    desc_field = item.value["Description"]
                    description = desc_field.value or ""

                if "Quantity" in item.value:
                    qty_field = item.value["Quantity"]
                    quantity = float(qty_field.value) if qty_field.value else 0.0

                if "Price" in item.value:
                    price_field = item.value["Price"]
                    price = float(price_field.value) if price_field.value else 0.0

                if "TotalPrice" in item.value:
                    tp_field = item.value["TotalPrice"]
                    total_price = float(tp_field.value) if tp_field.value else 0.0

                items.append(ReceiptItem(
                    description=description,
                    quantity=quantity,
                    price=price,
                    total_price=total_price
                ))

            if items_field.confidence:
                items_confidence = items_field.confidence

    overall_confidence = sum([
        merchant_confidence,
        tax_confidence,
        total_confidence,
        items_confidence
    ]) / 4.0 if any([merchant_confidence, tax_confidence, total_confidence, items_confidence]) else 0.0

    raw_fields = {
        "MerchantName": merchant_name,
        "TotalTax": tax_amount,
        "Total": total_amount,
        "ItemCount": len(items)
    }

    return ReceiptExtractionResult(
        merchant_name=merchant_name,
        tax_amount=tax_amount,
        total_amount=total_amount,
        items=items,
        confidence=overall_confidence,
        raw_fields=raw_fields
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = extract_receipt_fields(sys.argv[1])
        print(result.model_dump_json(indent=2))
