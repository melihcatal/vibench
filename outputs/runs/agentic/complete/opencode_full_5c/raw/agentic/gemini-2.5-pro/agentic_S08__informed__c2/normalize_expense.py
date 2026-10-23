from typing import Union
from document_models import Invoice, Receipt, Expense, LineItem
from google.cloud import firestore


def normalize_to_expense(document_data: Union[Invoice, Receipt]) -> Expense:
    """
    Normalizes an Invoice or Receipt object into a standard Expense object.
    Uses Google Cloud Firestore to look up a canonical vendor name.
    """
    db = firestore.Client()

    if isinstance(document_data, Invoice):
        vendor = document_data.vendor_name or "Unknown Vendor"
        date = document_data.invoice_date
        total = document_data.total_amount
        line_items = document_data.line_items
        source_type = "invoice"
    elif isinstance(document_data, Receipt):
        vendor = document_data.merchant_name or "Unknown Merchant"
        date = document_data.transaction_date
        total = document_data.total
        line_items = document_data.items
        source_type = "receipt"
    else:
        raise TypeError("Input document must be of type Invoice or Receipt")

    # Use Firestore to "normalize" the vendor name
    vendors_ref = db.collection("canonical_vendors")
    query = vendors_ref.where("aliases", "array_contains", vendor).limit(1)
    results = list(query.stream())

    canonical_name = vendor
    if results:
        canonical_name = results[0].to_dict().get("name", vendor)

    return Expense(
        vendor=canonical_name,
        date=str(date),
        total=float(total) if total is not None else 0.0,
        line_items=line_items,
        source_document_type=source_type,
    )
