import os
from document_client import get_document_intelligence_client
from document_models import ExpenseDocument, LineItem

def extract_receipt_fields(document_url: str) -> ExpenseDocument:
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document_from_url(
        "prebuilt-receipt", document_url
    )
    receipt_result = poller.result()

    merchant_name = None
    if receipt_result.documents and receipt_result.documents[0].fields.get("MerchantName"):
        merchant_name = receipt_result.documents[0].fields.get("MerchantName").value

    tax_amount = None
    if receipt_result.documents and receipt_result.documents[0].fields.get("TotalTax"):
        tax_amount = receipt_result.documents[0].fields.get("TotalTax").value

    total_amount = None
    if receipt_result.documents and receipt_result.documents[0].fields.get("Total"):
        total_amount = receipt_result.documents[0].fields.get("Total").value

    date = None
    if receipt_result.documents and receipt_result.documents[0].fields.get("TransactionDate"):
        date = str(receipt_result.documents[0].fields.get("TransactionDate").value)

    currency = None
    if receipt_result.documents and receipt_result.documents[0].fields.get("Total") and receipt_result.documents[0].fields.get("Total").currency_symbol:
        currency = receipt_result.documents[0].fields.get("Total").currency_symbol

    line_items = []
    if receipt_result.documents and receipt_result.documents[0].fields.get("Items"):
        for item in receipt_result.documents[0].fields.get("Items").value:
            description = item.value.get("Description").value if item.value.get("Description") else None
            quantity = item.value.get("Quantity").value if item.value.get("Quantity") else None
            amount = item.value.get("TotalPrice").value if item.value.get("TotalPrice") else None
            line_items.append(LineItem(description=description, quantity=quantity, amount=amount))

    return ExpenseDocument(
        document_type="receipt",
        merchant_name=merchant_name,
        date=date,
        tax_amount=tax_amount,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_response=receipt_result.to_dict()
    )
