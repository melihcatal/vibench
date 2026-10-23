import boto3
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse

def extract_invoice_fields(file_path: str) -> InvoiceExtractionResponse:
    # Using Amazon Textract AnalyzeExpense which returns structured invoice fields
    textract = boto3.client('textract')
    with open(file_path, 'rb') as f:
        document = {'Bytes': f.read()}
    # Call AnalyzeExpense (requires Business Intelligence tier)
    response = textract.analyze_expense(Document=document)
    # Map Textract response to our schema
    invoice = {
        'vendor': None,
        'date': None,
        'total': None,
        'line_items': []
    }
    # Simple extraction logic – you can replace with a more robust parser
    for block in response.get('ExpenseFields', []):
        label = block.get('Label')
        value = block.get('Value')
        if label:
            label_text = label.get('Text')
            value_text = value.get('Text')
            if 'Vendor' in label_text:
                invoice['vendor'] = value_text
            elif 'Date' in label_text:
                invoice['date'] = value_text
            elif 'Total' in label_text:
                invoice['total'] = value_text
    # Line items (very naive extraction)
    for item in response.get('ExpenseLineItems', []):
        invoice['line_items'].append({
            'description': item.get('Description', {}).get('Text'),
            'amount': item.get('Amount', {}).get('Text')
        })
    return InvoiceExtractionResponse(**invoice)
