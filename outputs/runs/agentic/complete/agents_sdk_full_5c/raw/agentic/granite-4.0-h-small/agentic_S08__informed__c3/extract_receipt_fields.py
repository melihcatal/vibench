import boto3
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse

def extract_receipt_fields(file_path: str) -> ReceiptExtractionResponse:
    # Using Mindee Invoice OCR (also works well for receipts)
    from mindee import MindeeClient
    client = MindeeClient(api_key="${MINDEE_API_KEY}")
    with open(file_path, 'rb') as f:
        result = client.invoice.process(f)
    receipt = {
        'merchant': None,
        'tax': None,
        'total': None,
        'items': []
    }
    # Extract merchant name (often in header)
    if result.document.merchant:
        receipt['merchant'] = result.document.merchant.name
    # Tax and total fields
    for field in result.document.parse.get('fields', []):
        if field.tag == 'total':
            receipt['total'] = field.value
        elif field.tag == 'tax':
            receipt['tax'] = field.value
    # Line items (if available)
    for line in result.document.parse.get('lines', []):
        receipt['items'].append({
            'description': line.description,
            'quantity': line.quantity,
            'unit_price': line.unit_price
        })
    return ReceiptExtractionResponse(**receipt)
