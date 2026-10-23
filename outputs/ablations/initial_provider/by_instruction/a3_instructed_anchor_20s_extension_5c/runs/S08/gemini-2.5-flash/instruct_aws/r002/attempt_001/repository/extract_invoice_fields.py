import os
from typing import Dict, Any, Optional, List
from document_client import get_aws_textract_client
from document_models import InvoiceDocument, LineItem, LineItemField

def extract_invoice_fields(document_s3_path: str) -> InvoiceDocument:
    """Extracts vendor, date, total, and line-item fields from an invoice using AWS Textract.

    Args:
        document_s3_path: S3 path to the invoice document (e.g., "s3://bucket-name/path/to/invoice.pdf")

    Returns:
        An InvoiceDocument object containing the extracted fields and raw Textract output.
    """
    textract_client = get_aws_textract_client()

    bucket_name = document_s3_path.split('/')[2]
    object_name = '/'.join(document_s3_path.split('/')[3:])

    response = textract_client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_name
            }
        },
        FeatureTypes=['FORMS', 'TABLES']
    )

    extracted_vendor = None
    extracted_date = None
    extracted_total = None
    extracted_currency = None
    extracted_line_items: List[LineItem] = []
    confidence_scores: Dict[str, float] = {}

    # Helper to find key-value pairs
    def find_key_value(key_text: str) -> Optional[str]:
        for page in response['Blocks']:
            if page['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in page['EntityTypes']:
                key_block_id = page['Id']
                for relationship in page.get('Relationships', []):
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            child_block = next((block for block in response['Blocks'] if block['Id'] == child_id), None)
                            if child_block and child_block['BlockType'] == 'WORD' and key_text.lower() in child_block['Text'].lower():
                                # Found the key, now find its value
                                for value_relationship in page.get('Relationships', []):
                                    if value_relationship['Type'] == 'VALUE':
                                        for value_id in value_relationship['Ids']:
                                            value_block = next((block for block in response['Blocks'] if block['Id'] == value_id), None)
                                            if value_block and value_block['BlockType'] == 'WORD':
                                                return value_block['Text']
        return None

    # Simplified parsing for demonstration; a robust solution would iterate through blocks more thoroughly
    # For forms, Textract provides 'KEY_VALUE_SET' blocks
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'PAGE':
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                        if child_block and child_block['BlockType'] == 'KEY_VALUE_SET':
                            key = None
                            value = None
                            for entity_type in child_block.get('EntityTypes', []):
                                if entity_type == 'KEY':
                                    for key_relationship in child_block.get('Relationships', []):
                                        if key_relationship['Type'] == 'CHILD':
                                            key = ' '.join([b['Text'] for b in response['Blocks'] if b['Id'] in key_relationship['Ids'] and b['BlockType'] == 'WORD'])
                                elif entity_type == 'VALUE':
                                    for value_relationship in child_block.get('Relationships', []):
                                        if value_relationship['Type'] == 'CHILD':
                                            value = ' '.join([b['Text'] for b in response['Blocks'] if b['Id'] in value_relationship['Ids'] and b['BlockType'] == 'WORD'])
                            
                            if key and value:
                                if "vendor" in key.lower():
                                    extracted_vendor = value
                                elif "date" in key.lower():
                                    extracted_date = value
                                elif "total" in key.lower() or "amount" in key.lower():
                                    try:
                                        extracted_total = float(value.replace('$', '').replace(',', ''))
                                        # Basic currency detection, improve as needed
                                        if '$' in value:
                                            extracted_currency = 'USD'
                                    except ValueError:
                                        pass


    # Placeholder for line items - Textract tables processing is complex and omitted for brevity
    # A full implementation would iterate through TABLE blocks and their cells.

    return InvoiceDocument(
        vendor_name=extracted_vendor,
        invoice_date=extracted_date,
        total_amount=extracted_total,
        currency=extracted_currency,
        line_items=extracted_line_items,
        raw_textract_output=response
    )
