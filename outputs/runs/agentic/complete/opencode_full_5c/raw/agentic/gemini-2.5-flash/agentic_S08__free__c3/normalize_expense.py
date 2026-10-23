from document_models import ExtractedDocument, NormalizedExpense, LineItem
from google.cloud import datastore
import os


def normalize_expense(extracted_doc: ExtractedDocument) -> NormalizedExpense:
    client = datastore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))

    normalized_expense = NormalizedExpense(
        original_document_type=extracted_doc.document_type
    )

    line_items = []
    current_line_item = LineItem()

    for field in extracted_doc.fields:
        if field.name == "vendor_name" or field.name == "merchant_name":
            # Example: Fetch canonical vendor name from Datastore
            query = client.query(kind="CanonicalVendor")
            query.add_filter("alias", "=", field.value)
            results = list(query.fetch())
            if results:
                normalized_expense.vendor_name = results[0].get("name")
            else:
                normalized_expense.vendor_name = field.value
        elif field.name == "invoice_date":
            normalized_expense.transaction_date = field.value
        elif field.name == "total_amount":
            try:
                normalized_expense.total_amount = float(field.value)
            except (ValueError, TypeError):
                pass
        elif field.name == "tax_amount":
            try:
                normalized_expense.tax_amount = float(field.value)
            except (ValueError, TypeError):
                pass
        elif field.name.startswith("line_item_") or field.name.startswith("item_"):
            if "description" in field.name:
                if current_line_item.description is not None:  # New line item
                    line_items.append(current_line_item)
                    current_line_item = LineItem()
                current_line_item.description = field.value
            elif "quantity" in field.name:
                try:
                    current_line_item.quantity = float(field.value)
                except (ValueError, TypeError):
                    pass
            elif "unit_price" in field.name:
                try:
                    current_line_item.unit_price = float(field.value)
                except (ValueError, TypeError):
                    pass
            elif "total_price" in field.name or "amount" in field.name:
                try:
                    current_line_item.total_price = float(field.value)
                except (ValueError, TypeError):
                    pass
    if (
        current_line_item.description
        or current_line_item.quantity
        or current_line_item.unit_price
        or current_line_item.total_price
    ):
        line_items.append(current_line_item)

    normalized_expense.line_items = line_items
    # Default currency to USD if not explicitly extracted and normalized
    normalized_expense.currency = "USD"  # Example default

    return normalized_expense
