import os
from document_client import get_document_intelligence_client
from document_models import NormalizedExpense, LineItem
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import Dict, Any, List

def extract_receipt_fields(document_url: str) -> NormalizedExpense:
    """
    Extracts merchant, tax, total, and items from a receipt using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-receipt", document_url
    )
    receipt_result: AnalyzeResult = poller.result()

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    line_items: List[LineItem] = []
    confidence_scores: Dict[str, float] = {}
    notes = None

    if receipt_result.documents:
        receipt = receipt_result.documents[0]

        if receipt.fields.get("MerchantName"):
            merchant_name = receipt.fields["MerchantName"].value
            confidence_scores["vendor_name"] = receipt.fields["MerchantName"].confidence
        if receipt.fields.get("TransactionDate"):
            transaction_date = receipt.fields["TransactionDate"].value.isoformat() if receipt.fields["TransactionDate"].value else None
            confidence_scores["transaction_date"] = receipt.fields["TransactionDate"].confidence
        if receipt.fields.get("TotalTax"):
            tax_amount = receipt.fields["TotalTax"].value
            confidence_scores["tax_amount"] = receipt.fields["TotalTax"].confidence
        if receipt.fields.get("Total"):
            total_amount = receipt.fields["Total"].value
            currency = receipt.fields["Total"].currency_symbol
            confidence_scores["total_amount"] = receipt.fields["Total"].confidence
        
        if receipt.fields.get("Items"):
            for item in receipt.fields["Items"].value:
                description = item.value.get("Description")
                quantity = item.value.get("Quantity")
                price = item.value.get("Price") # Receipt items usually have 'Price' not 'UnitPrice'
                total_price = item.value.get("TotalPrice")
                
                line_items.append(LineItem(
                    description=description.value if description else None,
                    quantity=quantity.value if quantity else None,
                    unit_price=price.value if price else None, # Map receipt price to unit_price
                    amount=total_price.value if total_price else None,
                ))
        
        if receipt.fields.get("Subtotal"): # Often receipts have subtotal, sometimes mapped to a 'notes' field if specific
            notes = f"Subtotal: {receipt.fields['Subtotal'].value}"
            confidence_scores["notes"] = receipt.fields["Subtotal"].confidence

    return NormalizedExpense(
        document_type="receipt",
        vendor_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=line_items,
        confidence_scores=confidence_scores,
        raw_document_path=document_url,
        notes=notes
    )
