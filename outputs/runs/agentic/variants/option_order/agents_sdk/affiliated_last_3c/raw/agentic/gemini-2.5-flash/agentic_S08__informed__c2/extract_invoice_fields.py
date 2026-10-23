import os
from document_client import get_document_intelligence_client
from document_models import NormalizedExpense, LineItem
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import Dict, Any, List

def extract_invoice_fields(document_url: str) -> NormalizedExpense:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-invoice", document_url
    )
    invoice_result: AnalyzeResult = poller.result()

    vendor_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    line_items: List[LineItem] = []
    confidence_scores: Dict[str, float] = {}
    notes = None

    if invoice_result.documents:
        invoice = invoice_result.documents[0]

        if invoice.fields.get("VendorName"):
            vendor_name = invoice.fields["VendorName"].value
            confidence_scores["vendor_name"] = invoice.fields["VendorName"].confidence
        if invoice.fields.get("InvoiceDate"):
            transaction_date = invoice.fields["InvoiceDate"].value.isoformat() if invoice.fields["InvoiceDate"].value else None
            confidence_scores["transaction_date"] = invoice.fields["InvoiceDate"].confidence
        if invoice.fields.get("TotalTax"):
            tax_amount = invoice.fields["TotalTax"].value
            confidence_scores["tax_amount"] = invoice.fields["TotalTax"].confidence
        if invoice.fields.get("InvoiceTotal"):
            total_amount = invoice.fields["InvoiceTotal"].value
            currency = invoice.fields["InvoiceTotal"].currency_symbol
            confidence_scores["total_amount"] = invoice.fields["InvoiceTotal"].confidence

        if invoice.fields.get("Items"):
            for item in invoice.fields["Items"].value:
                description = item.value.get("Description")
                quantity = item.value.get("Quantity")
                unit_price = item.value.get("UnitPrice")
                amount = item.value.get("Amount")
                
                line_items.append(LineItem(
                    description=description.value if description else None,
                    quantity=quantity.value if quantity else None,
                    unit_price=unit_price.value if unit_price else None,
                    amount=amount.value if amount else None,
                ))
        
        # Azure Document Intelligence does not have a dedicated 'notes' field for invoices
        # We can try to extract some generic text if needed, but for this exercise, we'll keep it simple.
        # For demonstration, let's assume 'CustomerName' could sometimes contain notes if misused.
        # This is a placeholder and would need proper mapping based on actual document structure.
        if invoice.fields.get("CustomerName"):
            notes = invoice.fields["CustomerName"].value
            confidence_scores["notes"] = invoice.fields["CustomerName"].confidence


    return NormalizedExpense(
        document_type="invoice",
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=line_items,
        confidence_scores=confidence_scores,
        raw_document_path=document_url,
        notes=notes
    )
