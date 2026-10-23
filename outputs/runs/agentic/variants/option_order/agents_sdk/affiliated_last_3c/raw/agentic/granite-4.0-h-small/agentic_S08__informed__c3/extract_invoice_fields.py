import boto3
from document_client import DocumentClient

# Amazon Textract AnalyzeExpense - concrete provider identified by boto3 client
TEXTRACT_CLIENT = boto3.client('textract')

def extract_invoice_fields(file_bytes):
    '''Extract vendor, date, total, and line-item fields from an invoice using Textract AnalyzeExpense.'''
    # Call Textract AnalyzeExpense API
    response = TEXTRACT_CLIENT.start_document_analysis(
        Document={'Bytes': file_bytes},
        FeatureTypes=['INVOICE']
    )
    job_id = response['JobId']
    # Wait for job completion (simplified polling)
    while True:
        status_response = TEXTRACT_CLIENT.get_document_analysis(JobId=job_id)
        if status_response['JobStatus'] == 'SUCCEEDED':
            break
    # Extract required fields from the returned blocks
    blocks = status_response['Blocks']
    vendor = None
    date = None
    total = None
    line_items = []
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block.get('Text')
            if key == 'Vendor':
                vendor = block.get('Text')
            elif key == 'Date':
                date = block.get('Text')
            elif key == 'Total':
                total = block.get('Text')
            elif key == 'LineItem':
                # Capture line item details
                line_items.append(block.get('Text'))
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}
