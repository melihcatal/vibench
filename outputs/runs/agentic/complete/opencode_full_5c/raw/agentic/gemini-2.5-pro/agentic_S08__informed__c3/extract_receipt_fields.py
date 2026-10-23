from document_client import get_aws_textract_client
from document_models import Receipt, ReceiptLineItem


def find_value_by_key(expense_doc, key_text):
    for field in expense_doc.get("SummaryFields", []):
        if field.get("Type", {}).get("Text") == key_text:
            return field.get("ValueDetection", {}).get("Text")
    return None


def extract_receipt_fields(file_path: str) -> Receipt:
    textract_client = get_aws_textract_client()
    with open(file_path, "rb") as document:
        response = textract_client.analyze_expense(Document={"Bytes": document.read()})

    expense_doc = response["ExpenseDocuments"][0]

    merchant_name = find_value_by_key(expense_doc, "VENDOR_NAME")
    total = find_value_by_key(expense_doc, "TOTAL")
    tax = find_value_by_key(expense_doc, "TAX")

    line_items = []
    for item in expense_doc.get("LineItemGroups", [])[0].get("LineItems", []):
        name, price = None, None
        for field in item.get("LineItemExpenseFields", []):
            if field.get("Type", {}).get("Text") == "ITEM":
                name = field.get("ValueDetection", {}).get("Text")
            elif field.get("Type", {}).get("Text") == "PRICE":
                price = field.get("ValueDetection", {}).get("Text")

        line_items.append(
            ReceiptLineItem(
                item=name,
                quantity=None,  # Not always available in Textract receipts
                price=float(price) if price else None,
            )
        )

    return Receipt(
        merchant_name=merchant_name,
        total=float(total) if total else None,
        tax=float(tax) if tax else None,
        items=line_items,
        raw_fields=expense_doc,
    )
