from azure.ai.formrecognizer import DocumentAnalysisClient
from document_client import get_document_intelligence_client
from document_models import ExtractedReceipt, ReceiptItem


def extract_receipt_fields(file_path: str) -> ExtractedReceipt:
    """
    Extracts structured data from a receipt using Azure AI Document Intelligence.
    """
    client = get_document_intelligence_client()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-receipt", document=f.read()
        )
    receipts = poller.result()

    if not receipts.documents:
        return ExtractedReceipt()
        
    receipt = receipts.documents[0]

    def get_field_value(field_name):
        field = receipt.fields.get(field_name)
        return field.value if field else None
    
    extracted_items = []
    items_field = receipt.fields.get("Items")
    if items_field and items_field.value:
        for item_doc in items_field.value:
            item = {}
            if item_doc.value.get("Description"):
                item["description"] = item_doc.value["Description"].value
            if item_doc.value.get("TotalPrice"):
                 item["total_price"] = item_doc.value["TotalPrice"].value
            if item_doc.value.get("Quantity"):
                 item["quantity"] = item_doc.value["Quantity"].value
            extracted_items.append(ReceiptItem(**item))

    extracted_data = {
        "merchant_name": get_field_value("MerchantName"),
        "transaction_date": str(get_field_value("TransactionDate")),
        "tax": get_field_value("TotalTax"),
        "total": get_field_value("Total"),
        "items": extracted_items,
        "raw_fields": {f.name: f.content for f in receipt.fields.values() if f.content is not None}
    }

    return ExtractedReceipt(**extracted_data)
