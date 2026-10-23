import os
from document_client import get_textract_client
from document_models import Receipt, ReceiptItem


def extract_receipt_fields(file_path: str) -> Receipt:
    """
    Extracts fields from a receipt document using Amazon Textract.
    """
    textract_client = get_textract_client()

    with open(file_path, "rb") as document:
        response = textract_client.analyze_expense(Document={"Bytes": document.read()})

    receipt = Receipt()
    receipt.raw_fields = response

    for expense_doc in response.get("ExpenseDocuments", []):
        for field in expense_doc.get("SummaryFields", []):
            field_type = field.get("Type", {}).get("Text")
            value = field.get("ValueDetection", {}).get("Text")

            if field_type == "MERCHANT_NAME":
                receipt.merchant_name = value
            elif field_type == "TOTAL":
                try:
                    receipt.total_amount = float(value.replace("$", ""))
                except (ValueError, TypeError):
                    receipt.total_amount = None
            elif field_type == "TAX":
                try:
                    receipt.tax_amount = float(value.replace("$", ""))
                except (ValueError, TypeError):
                    receipt.tax_amount = None

        for item in expense_doc.get("LineItemGroups", [])[0].get("LineItems", []):
            receipt_item = ReceiptItem()
            for field in item.get("LineItemExpenseFields", []):
                field_type = field.get("Type", {}).get("Text")
                value = field.get("ValueDetection", {}).get("Text")
                if field_type == "ITEM":
                    receipt_item.item_name = value
                elif field_type == "PRICE":
                    try:
                        receipt_item.item_price = float(value.replace("$", ""))
                    except (ValueError, TypeError):
                        receipt_item.item_price = None
                elif field_type == "QUANTITY":
                    try:
                        receipt_item.item_quantity = float(value)
                    except (ValueError, TypeError):
                        receipt_item.item_quantity = None
            if any(vars(receipt_item).values()):
                receipt.items.append(receipt_item)

    return receipt
