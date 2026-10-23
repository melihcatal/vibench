import boto3

# AWS SDK (boto3) used for Amazon Textract AnalyzeExpense (also works for receipt OCR)
client = boto3.client('textract')

def extract_receipt_fields(receipt_bytes):
    # Call Textract AnalyzeExpense (or you could use a dedicated receipt extraction API)
    response = client.analyze_expense(
        Document={'Bytes': receipt_bytes}
    )
    # Simple extraction logic – flesh out with actual receipt field parsing
    result = {
        'merchant': None,
        'tax': None,
        'total': None,
        'items': []
    }
    # Placeholder – replace with real extraction from response
    return result