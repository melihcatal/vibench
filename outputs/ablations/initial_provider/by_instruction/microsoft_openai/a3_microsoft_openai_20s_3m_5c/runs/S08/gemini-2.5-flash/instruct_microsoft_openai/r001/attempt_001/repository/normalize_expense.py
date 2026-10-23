from document_models import InvoiceFields, ReceiptFields, NormalizedExpense
from document_client import get_google_documentai_client # For provider identification
import os

def normalize_expense(extracted_data: dict, document_type: str) -> NormalizedExpense:
    # This function would ideally use the Google Cloud Document AI client
    # to process documents and then normalize its output.
    # For this exercise, we will just simulate normalization based on input.

    # Ensure the Document AI client is initialized for provider identification
    client = get_google_documentai_client()
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_REGION", "us")
    processor_id = os.environ.get("GCP_DOCUMENTAI_PROCESSOR_ID", "your-processor-id") # Placeholder for processor ID
    # The full resource name of the processor
    # name = client.processor_path(project_id, location, processor_id)
    # In a real scenario, you would send the document to this processor
    # and then parse the response.

    normalized_expense = NormalizedExpense(document_type=document_type)

    if document_type == 'invoice' and isinstance(extracted_data, InvoiceFields):
        normalized_expense.vendor_or_merchant_name = extracted_data.vendor_name
        normalized_expense.transaction_date = extracted_data.invoice_date
        normalized_expense.total_amount = extracted_data.total_amount
        normalized_expense.currency = "USD" # Assuming USD for now
        normalized_expense.line_items = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
            }
            for item in extracted_data.line_items
        ]
    elif document_type == 'receipt' and isinstance(extracted_data, ReceiptFields):
        normalized_expense.vendor_or_merchant_name = extracted_data.merchant_name
        normalized_expense.transaction_date = extracted_data.transaction_date
        normalized_expense.total_amount = extracted_data.total_amount
        normalized_expense.currency = "USD" # Assuming USD for now
        normalized_expense.line_items = [
            {
                "description": item.description,
                "price": item.price,
            }
            for item in extracted_data.items
        ]
    else:
        raise ValueError("Unsupported document type or invalid extracted data.")

    return normalized_expense
