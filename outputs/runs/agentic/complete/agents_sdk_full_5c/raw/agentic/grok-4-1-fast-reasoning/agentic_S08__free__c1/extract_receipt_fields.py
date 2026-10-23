import os
import boto3
from document_models import ExtractedReceipt
from document_client import get_aws_region

def extract_receipt_fields(image_bytes: bytes) -> ExtractedReceipt:
    textract = boto3.client('textract', region_name=get_aws_region())

    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )

    form_key_map = {}
    confidences = {}

    def get_block_text(block_id: str) -> str:
        for block in response['Blocks']:
            if block['Id'] == block_id:
                return block['Text']
        return ''

    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
            key = block['Text'].lower()
            if block['Relationships']:
                rel = block['Relationships'][0]
                if rel['Type'] == 'CHILD':
                    val_id = rel['Ids'][0]
                    val = get_block_text(val_id)
                    form_key_map[key] = val
                    confidences[key] = block.get('Confidence', 0.0)

    merchant = form_key_map.get('merchant') or form_key_map.get('store')
    tax = float(form_key_map.get('tax', 0).replace('$', '')) if form_key_map.get('tax') else None
    total = float(form_key_map.get('total', 0).replace('$', '')) if form_key_map.get('total') else None
    items = list(form_key_map.get('item', '').split(', '))  # simplistic

    return ExtractedReceipt(
        merchant=merchant,
        tax=tax,
        total=total,
        items=items,
        confidence=confidences
    )
