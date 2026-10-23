from document_client import DocumentClient
from document_models import ReceiptFields, LineItem
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, ContentFormat
from typing import Dict, Any, List, Optional

def extract_receipt_fields(document_path: str) -> ReceiptFields:
    doc_client = DocumentClient()
    client = doc_client.get_client()

    with open(document_path, "rb") as f: # type: ignore
        poller = client.begin_analyze_document(
            "prebuilt-receipt",
            f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    receipt_fields = ReceiptFields()
    if result.documents and len(result.documents) > 0:
        receipt = result.documents[0]
        if receipt.fields:
            receipt_fields.merchant_name = receipt.fields.get("MerchantName")?.value if receipt.fields.get("MerchantName") else None  # type: ignore
            receipt_fields.transaction_date = receipt.fields.get("TransactionDate")?.value if receipt.fields.get("TransactionDate") else None # type: ignore
            receipt_fields.tax_amount = receipt.fields.get("TotalTax")?.value if receipt.fields.get("TotalTax") else None # type: ignore
            receipt_fields.total_amount = receipt.fields.get("Total")?.value if receipt.fields.get("Total") else None # type: ignore
            
            if receipt.fields.get("Items"):
                for item in receipt.fields["Items"].value:
                    line_item = LineItem(
                        description=item.value.get("Description")?.value if item.value.get("Description") else None, # type: ignore
                        quantity=item.value.get("Quantity")?.value if item.value.get("Quantity") else None, # type: ignore
                        unit_price=item.value.get("UnitPrice")?.value if item.value.get("UnitPrice") else None, # type: ignore
                        amount=item.value.get("TotalAmount")?.value if item.value.get("TotalAmount") else None # type: ignore
                    )
                    receipt_fields.line_items.append(line_item)
    return receipt_fields
