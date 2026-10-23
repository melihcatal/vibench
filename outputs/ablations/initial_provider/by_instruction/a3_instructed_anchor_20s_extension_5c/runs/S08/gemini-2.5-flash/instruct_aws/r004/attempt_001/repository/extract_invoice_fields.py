import boto3
from typing import Dict, Any, List, Optional
from document_models import ExtractedInvoice

def _get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '
    return text

def extract_invoice_fields(image_bytes: bytes) -> ExtractedInvoice:
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )

    blocks = response['Blocks']
    blocks_map = {block['Id']: block for block in blocks}
    key_value_pairs = {}

    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key_text = _get_text(block, blocks_map)
                value_text = ''
                if 'Relationships' in block:
                    for relationship in block['Relationships']:
                        if relationship['Type'] == 'VALUE':
                            for value_id in relationship['Ids']:
                                value_block = blocks_map[value_id]
                                value_text = _get_text(value_block, blocks_map)
                key_value_pairs[key_text.strip()] = value_text.strip()

    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[Dict[str, Any]] = []

    for key, value in key_value_pairs.items():
        lower_key = key.lower()
        if 'vendor name' in lower_key or 'seller name' in lower_key or 'company' in lower_key:
            vendor_name = value
        elif 'invoice date' in lower_key or 'date' in lower_key:
            invoice_date = value
        elif 'total' in lower_key or 'amount due' in lower_key or 'balance due' in lower_key:
            try:
                cleaned_value = value.replace('$', '').replace(',', '').strip()
                total_amount = float(cleaned_value)
            except ValueError:
                pass

    return ExtractedInvoice(
        vendor_name=vendor_name,
        invoice_date=invoice_date,
        total_amount=total_amount,
        line_items=line_items,
    )
