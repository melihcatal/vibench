import boto3
import os
from typing import Dict, Any, List
from document_models import ExtractedInvoice, LineItem
from document_client import load_document

def extract_invoice_fields(file_path: str) -> ExtractedInvoice:
    textract = boto3.client(
        'textract',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    document = {'Bytes': load_document(file_path)}
    response = textract.analyze_expense(
        Document=document,
        FeatureTypes=['EXPENSE']
    )
    # Parse response
    block_map: Dict[str, Dict] = {block['Id']: block for block in response['Blocks']}
    fields: Dict[str, Any] = {}
    confidences: Dict[str, float] = {}
    line_items: List[LineItem] = []
    for block in response['Blocks']:
        if 'EntityTypes' in block:
            entity_types = block['EntityTypes']
            text = block.get('Text', '')
            confidence = block['Confidence']
            if 'VENDOR_NAME' in entity_types:
                fields['vendor'] = text
                confidences['vendor'] = confidence
            elif 'INVOICE_DATE' in entity_types:
                fields['date'] = text
                confidences['date'] = confidence
            elif 'TOTAL' in entity_types:
                # Simple parsing
                total_str = text.replace('$', '').replace(',', '')
                fields['total'] = float(total_str)
                confidences['total'] = confidence
            elif 'LINE_ITEM_GROUP' in entity_types:
                # Simplified line item extraction
                for relationship in block.get('Relationships', []):
                    if relationship['Type'] == 'CHILD':
                        for child_id in relationship['Ids']:
                            child_block = block_map.get(child_id)
                            if child_block and 'LINE_ITEM' in child_block.get('EntityTypes', []):
                                item_text = child_block.get('Text', '')
                                line_items.append({
                                    'description': item_text,
                                    'quantity': None,
                                    'unit_price': None,
                                    'amount': 0.0
                                })
    return ExtractedInvoice(
        vendor=fields.get('vendor', ''),
        date=fields.get('date', ''),
        total=fields.get('total', 0.0),
        line_items=line_items,
        confidence=confidences
    )
