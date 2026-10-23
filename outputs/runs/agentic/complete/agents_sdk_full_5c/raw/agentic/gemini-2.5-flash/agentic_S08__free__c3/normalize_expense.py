
from google.cloud import datacatalog
import json
import os
from document_models import ExpenseRecord

def normalize_expense(extracted_data: dict, document_type: str) -> ExpenseRecord:
    """
    Normalizes extracted expense fields into a standard JSON schema,
    conceptually fetching schema from Google Cloud Data Catalog.
    """
    # In a real scenario, you'd retrieve a schema from Data Catalog.
    # For this example, we'll simulate fetching a generic expense schema
    # and directly apply normalization logic based on expected input.

    # This is a simplified example. A real implementation would query Data Catalog
    # to retrieve a schema, e.g., for an expense record template.
    # client = datacatalog.DataCatalogClient()
    # tag_template_name = client.tag_template_path(
    #     project=os.getenv("GCP_PROJECT_ID"),
    #     location=os.getenv("GCP_LOCATION", "us-central1"),
    #     tag_template=os.getenv("DATACATALOG_EXPENSE_SCHEMA_ID")
    # )
    # tag_template = client.get_tag_template(name=tag_template_name)
    # print(f"Simulating schema retrieval from Data Catalog: {tag_template.display_name}")

    normalized_record = ExpenseRecord()
    normalized_record.document_type = document_type

    if document_type == "invoice":
        normalized_record.vendor_name = extracted_data.get("vendor_name")
        normalized_record.transaction_date = extracted_data.get("invoice_date")
        normalized_record.total_amount = float(extracted_data.get("total_amount", 0.0))
        for item in extracted_data.get("line_items", []):
            normalized_record.line_items.append({
                "description": item.get("description"),
                "amount": float(item.get("amount", 0.0)),
                "quantity": int(item.get("quantity", 1))
            })
    elif document_type == "receipt":
        normalized_record.vendor_name = extracted_data.get("merchant_name")
        # Receipts often don't have a distinct 'invoice_date', use current date or best guess
        normalized_record.transaction_date = extracted_data.get("receipt_date") # Assuming receipt_date might be extracted by Textract
        normalized_record.total_amount = float(extracted_data.get("total_amount", 0.0))
        normalized_record.tax_amount = float(extracted_data.get("tax_amount", 0.0))
        for item in extracted_data.get("items", []):
            normalized_record.line_items.append({
                "description": item.get("description"),
                "amount": float(item.get("amount", 0.0)),
                "quantity": int(item.get("quantity", 1)) # Textract might not always provide quantity directly in line items
            })

    return normalized_record

if __name__ == '__main__':
    # Example invoice data
    invoice_extracted = {
        "vendor_name": "Example Corp",
        "invoice_date": "2023-10-26",
        "total_amount": "123.45",
        "line_items": [
            {"description": "Item A", "amount": "100.00", "quantity": "1"},
            {"description": "Tax", "amount": "23.45", "quantity": "1"}
        ]
    }
    normalized_invoice = normalize_expense(invoice_extracted, "invoice")
    print("Normalized Invoice:", normalized_invoice.model_dump_json(indent=2))

    # Example receipt data
    receipt_extracted = {
        "merchant_name": "Coffee Shop",
        "receipt_date": "2023-10-26",
        "total_amount": "5.50",
        "tax_amount": "0.50",
        "items": [
            {"description": "Coffee", "amount": "5.00"}
        ]
    }
    normalized_receipt = normalize_expense(receipt_extracted, "receipt")
    print("Normalized Receipt:", normalized_receipt.model_dump_json(indent=2))
