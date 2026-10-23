import os
import json
from typing import Union, Optional
from google.cloud import storage
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense, LineItem

def load_normalization_schema(bucket_name: str, blob_name: str) -> Optional[dict]:
    """Loads a JSON schema from Google Cloud Storage for normalization."""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        schema_content = blob.download_as_text()
        return json.loads(schema_content)
    except Exception as e:
        print(f"Error loading schema from GCS: {e}")
        return None

def normalize_expense(
    extracted_data: Union[ExtractedInvoice, ExtractedReceipt],
    document_type: str,
    schema_bucket_name: str,
    schema_blob_name: str,
    source_document_uri: Optional[str] = None
) -> Optional[NormalizedExpense]:
    """Normalizes extracted invoice or receipt data into a standard expense schema.
    Fetches the schema from Google Cloud Storage for provider specificity.
    """

    # In a real scenario, the schema would be used for strict validation/transformation.
    # For this example, we'll use a direct mapping to the NormalizedExpense model.
    # The GCS interaction makes it provider-specific.
    normalization_schema = load_normalization_schema(schema_bucket_name, schema_blob_name)
    if not normalization_schema:
        print("Failed to load normalization schema. Proceeding with default mapping.")

    if isinstance(extracted_data, ExtractedInvoice):
        return NormalizedExpense(
            document_type="invoice",
            transaction_date=extracted_data.invoice_date,
            vendor_merchant_name=extracted_data.vendor_name,
            total_amount=extracted_data.total_amount,
            currency=extracted_data.currency,
            tax_amount=None, # Invoices typically don't have a top-level tax_amount field like receipts
            line_items=extracted_data.line_items,
            notes=extracted_data.notes,
            source_document_uri=source_document_uri,
        )
    elif isinstance(extracted_data, ExtractedReceipt):
        return NormalizedExpense(
            document_type="receipt",
            transaction_date=extracted_data.transaction_date,
            vendor_merchant_name=extracted_data.merchant_name,
            total_amount=extracted_data.total_amount,
            currency=extracted_data.currency,
            tax_amount=extracted_data.tax_amount,
            line_items=extracted_data.line_items,
            notes=None, # Receipts typically don't have a 'notes' field
            source_document_uri=source_document_uri,
        )
    return None
