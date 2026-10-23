from document_client import get_aws_textract_client
from document_models import ReceiptFields, ReceiptItem

def extract_receipt_fields(document_bytes: bytes) -> ReceiptFields:
    client = get_aws_textract_client()

    response = client.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=['FORMS'] # Using FORMS for structured data extraction
    )

    # Placeholder for parsing Textract response into ReceiptFields
    # This part would involve iterating through Blocks and extracting key-value pairs
    # For this exercise, we will just create a dummy ReceiptFields object
    receipt_fields = ReceiptFields()
    receipt_fields.merchant_name = "Extracted Merchant Example"
    receipt_fields.total_amount = 123.45
    receipt_fields.transaction_date = "2026-09-20"
    receipt_fields.tax_amount = 10.00
    receipt_fields.items.append(ReceiptItem(description="Item A", price=100.00))
    receipt_fields.items.append(ReceiptItem(description="Item B", price=13.45))

    return receipt_fields
