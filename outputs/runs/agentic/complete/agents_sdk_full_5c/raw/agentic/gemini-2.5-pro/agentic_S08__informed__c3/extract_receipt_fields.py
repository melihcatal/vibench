from document_client import get_document_client
from document_models import Receipt, ReceiptItem

def extract_receipt(file_path: str) -> Receipt:
    """
    Extracts fields from a receipt document using Azure Document Intelligence.
    """
    client = get_document_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-receipt", document=f)
    
    result = poller.result()
    receipt_data = Receipt()

    if result.documents:
        doc = result.documents[0]
        receipt_data.confidence = doc.confidence
        fields = doc.fields
        
        merchant_name_field = fields.get("MerchantName")
        if merchant_name_field and merchant_name_field.value_string:
            receipt_data.merchant_name = merchant_name_field.value_string

        date_field = fields.get("TransactionDate")
        if date_field and date_field.value_date:
            receipt_data.transaction_date = str(date_field.value_date)

        total_field = fields.get("Total")
        if total_field and total_field.value_amount:
            receipt_data.total = total_field.value_amount.amount
        
        tax_field = fields.get("TotalTax")
        if tax_field and tax_field.value_amount:
            receipt_data.tax = tax_field.value_amount.amount

        items_field = fields.get("Items")
        if items_field and items_field.value_array:
            for item_value in items_field.value_array:
                if item_value.value_object:
                    item_fields = item_value.value_object
                    receipt_item = ReceiptItem(
                        description=item_fields.get("Description", {}).get("value_string"),
                        quantity=item_fields.get("Quantity", {}).get("value_number"),
                        price=item_fields.get("TotalPrice", {}).get("value_amount", {}).get("amount"),
                    )
                    receipt_data.items.append(receipt_item)
    
    return receipt_data
