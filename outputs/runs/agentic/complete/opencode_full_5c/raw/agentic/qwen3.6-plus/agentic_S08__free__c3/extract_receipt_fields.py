import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import ReceiptExtraction


def extract_receipt_fields(document_bytes: bytes) -> ReceiptExtraction:
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://your-resource.cognitiveservices.azure.com/",
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    credential = AzureKeyCredential(key)
    client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)

    poller = client.begin_analyze_document("prebuilt-receipt", document_bytes)
    result = poller.result()

    receipts = result.documents
    if not receipts:
        raise ValueError("No receipt data found in the document")

    receipt = receipts[0]
    fields = receipt.fields

    merchant_name = fields.get("MerchantName", {}).get("value", "")
    transaction_date = fields.get("TransactionDate", {}).get("value", "")
    total_amount = fields.get("Total", {}).get("value", 0.0)
    tax_amount = fields.get("TotalTax", {}).get("value", 0.0)
    currency = fields.get("CurrencyCode", {}).get("value", "USD")

    confidence_scores = {}
    for field_name in [
        "MerchantName",
        "TransactionDate",
        "Total",
        "TotalTax",
        "CurrencyCode",
    ]:
        f = fields.get(field_name)
        if f and f.confidence is not None:
            confidence_scores[field_name] = f.confidence

    items = []
    items_field = fields.get("Items", {})
    if items_field and items_field.get("value"):
        for item in items_field["value"]:
            item_fields = item.get("value", {})
            items.append(
                {
                    "description": item_fields.get("Description", {}).get("value", ""),
                    "quantity": item_fields.get("Quantity", {}).get("value", 0.0),
                    "price": item_fields.get("Price", {}).get("value", 0.0),
                    "total_price": item_fields.get("TotalPrice", {}).get("value", 0.0),
                }
            )

    return ReceiptExtraction(
        merchant_name=merchant_name,
        transaction_date=str(transaction_date) if transaction_date else "",
        total_amount=float(total_amount) if total_amount else 0.0,
        tax_amount=float(tax_amount) if tax_amount else 0.0,
        currency=currency,
        items=items,
        confidence_scores=confidence_scores,
    )
