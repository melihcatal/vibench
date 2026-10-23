from document_client import get_document_intelligence_client
from document_models import Receipt, ReceiptLineItem


def extract_receipt_fields_from_url(receipt_url: str) -> Receipt:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-receipt", analyze_request={"urlSource": receipt_url}
    )
    result = poller.result()

    receipt_data = {}
    line_items_data = []

    if result.documents:
        document = result.documents[0]
        receipt_data["raw_fields"] = {
            name: field.to_dict() for name, field in document.fields.items()
        }

        merchant_name = document.fields.get("MerchantName")
        if merchant_name:
            receipt_data["merchant_name"] = merchant_name.get("content")

        transaction_date = document.fields.get("TransactionDate")
        if transaction_date:
            receipt_data["transaction_date"] = str(transaction_date.get("value"))

        tax = document.fields.get("TotalTax")
        if tax:
            receipt_data["tax"] = tax.get("value").amount if tax.get("value") else None

        total = document.fields.get("Total")
        if total:
            receipt_data["total"] = (
                total.get("value").amount if total.get("value") else None
            )

        items = document.fields.get("Items")
        if items and items.get("value"):
            for item in items.get("value"):
                item_fields = item.get("value")
                line_item = ReceiptLineItem(
                    description=item_fields.get("Description").get("content")
                    if item_fields.get("Description")
                    else None,
                    quantity=item_fields.get("Quantity").get("value")
                    if item_fields.get("Quantity")
                    else None,
                    total_price=item_fields.get("TotalPrice").get("value").amount
                    if item_fields.get("TotalPrice")
                    and item_fields.get("TotalPrice").get("value")
                    else None,
                )
                line_items_data.append(line_item)

    receipt_data["line_items"] = line_items_data
    return Receipt(**receipt_data)
