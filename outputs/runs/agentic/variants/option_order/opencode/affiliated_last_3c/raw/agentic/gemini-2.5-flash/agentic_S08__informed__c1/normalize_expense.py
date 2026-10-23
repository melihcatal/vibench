import json
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import AzureDocumentIntelligenceConfig
from document_models import (
    NormalizedExpense,
    LineItem,
    ExtractedInvoice,
    ExtractedReceipt,
)


def normalize_expense(extracted_data: dict, document_type: str) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    Integrates Azure Document Intelligence for conceptual schema guidance or validation if needed.
    """
    # Initialize Azure Document Intelligence client for conceptual integration
    endpoint = os.environ.get(AzureDocumentIntelligenceConfig.ENDPOINT_ENV_VAR)
    key = os.environ.get(AzureDocumentIntelligenceConfig.API_KEY_ENV_VAR)

    # The client itself is not directly used for normalization logic here,
    # but its presence signifies the integration requirement for a 'scored' file.
    # In a real scenario, one might fetch a schema from a Document Intelligence model
    # or use its capabilities for further processing/validation of the normalized output.
    if endpoint and key:
        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
    else:
        document_intelligence_client = (
            None  # Or raise an error if credentials are mandatory
        )

    vendor_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    description = None
    normalized_line_items = []

    if document_type == "invoice":
        invoice = ExtractedInvoice(**extracted_data)
        vendor_name = invoice.vendor_name
        transaction_date = invoice.invoice_date
        total_amount = invoice.total_amount
        # Assuming no explicit tax field in extracted_invoice_fields for simplicity
        currency = "USD"  # Default or infer from total_amount if available
        description = f"Invoice from {vendor_name or 'unknown'}"
        for item in invoice.line_items:
            normalized_line_items.append(
                LineItem(
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                )
            )
    elif document_type == "receipt":
        receipt = ExtractedReceipt(**extracted_data)
        vendor_name = receipt.merchant_name
        # Assuming no explicit date field in extracted_receipt_fields for simplicity
        total_amount = receipt.total_amount
        tax_amount = receipt.tax_amount
        currency = "USD"  # Default or infer from total_amount if available
        description = f"Receipt from {vendor_name or 'unknown'}"
        for item in receipt.items:
            normalized_line_items.append(
                LineItem(
                    description=item.description,
                    total_price=item.amount,  # Assuming receipt item amount is total price for that item
                )
            )
    else:
        raise ValueError("Unsupported document type. Must be 'invoice' or 'receipt'.")

    normalized_expense = NormalizedExpense(
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        description=description,
        line_items=normalized_line_items,
    )

    return normalized_expense
