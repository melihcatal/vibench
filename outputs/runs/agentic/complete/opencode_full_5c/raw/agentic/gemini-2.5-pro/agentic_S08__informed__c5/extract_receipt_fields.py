from document_client import get_document_intelligence_client
from document_models import Receipt, ReceiptItem


def extract_receipt_fields(file_path: str) -> Receipt:
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-receipt",
            analyze_request=f,
            content_type="application/octet-stream",
        )

    receipts = poller.result()

    if not receipts.documents:
        return Receipt()

    doc = receipts.documents[0]

    merchant_name = doc.fields.get("MerchantName")
    transaction_date = doc.fields.get("TransactionDate")
    total = doc.fields.get("Total")
    tax = doc.fields.get("TotalTax")

    extracted_items = []
    items_field = doc.fields.get("Items")
    if items_field and items_field.kind == "list":
        for item in items_field.value:
            if item.kind == "dictionary":
                description = item.value.get("Description")
                quantity = item.value.get("Quantity")
                price = item.value.get("Price")
                total_price = item.value.get("TotalPrice")

                extracted_items.append(
                    ReceiptItem(
                        description=description.value if description else None,
                        quantity=quantity.value if quantity else None,
                        price=price.value if price else None,
                        total_price=total_price.value if total_price else None,
                    )
                )

    return Receipt(
        merchant_name=merchant_name.value if merchant_name else "N/A",
        transaction_date=str(transaction_date.value) if transaction_date else "N/A",
        total=total.value if total else 0.0,
        tax=tax.value if tax else 0.0,
        items=extracted_items,
    )
