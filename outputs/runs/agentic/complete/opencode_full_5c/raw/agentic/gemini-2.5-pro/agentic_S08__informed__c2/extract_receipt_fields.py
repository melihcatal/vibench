from document_client import get_document_client
from document_models import Receipt, LineItem


def extract_receipt(file_path: str) -> Receipt:
    """
    Extracts fields from a receipt document using Azure Document Intelligence.
    """
    client = get_document_client()

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
    merchant_address = doc.fields.get("MerchantAddress")
    transaction_date = doc.fields.get("TransactionDate")
    transaction_time = doc.fields.get("TransactionTime")
    total = doc.fields.get("Total")
    tax = doc.fields.get("TotalTax")

    extracted_receipt = Receipt(
        merchant_name=merchant_name.value if merchant_name else None,
        merchant_address=merchant_address.content if merchant_address else None,
        transaction_date=str(transaction_date.value) if transaction_date else None,
        transaction_time=str(transaction_time.value) if transaction_time else None,
        total=total.value.amount if total and total.value else None,
        tax=tax.value.amount if tax and tax.value else None,
        raw_document=doc.to_dict(),
    )

    items_field = doc.fields.get("Items")
    if items_field and items_field.value:
        for item in items_field.value:
            line_item = LineItem(
                description=item.value.get("Description", {}).get("value"),
                quantity=item.value.get("Quantity", {}).get("value"),
                total_price=item.value.get("TotalPrice", {})
                .get("value", {})
                .get("amount"),
            )
            extracted_receipt.items.append(line_item)

    return extracted_receipt
