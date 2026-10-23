import boto3
from typing import Dict, Any
from document_models import ReceiptFields
from document_client import get_aws_region

def extract_receipt_fields(image_bytes: bytes) -> Dict[str, Any]:
    textract = boto3.client('textract', region_name=get_aws_region())
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS', 'TABLES']
    )

    # Simplified key-value extraction using relationships
    key_map = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in block:
            if block['EntityTypes'][0] == 'KEY':
                key_id = block['Id']
                key_map[key_id] = block['Text'].lower()

    fields = {'items': []}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'EntityTypes' in block and block['EntityTypes'][0] == 'VALUE':
            if 'Relationships' in block:
                for rel in block['Relationships']:
                    if rel['Type'] == 'CHILD':
                        for kid in rel['Ids']:
                            if kid in key_map:
                                key = key_map[kid]
                                value = block['Text']
                                if 'merchant' in key or 'store' in key:
                                    fields['merchant'] = value
                                elif 'total' in key:
                                    fields['total'] = float(value.replace('$', '').replace(',', ''))
                                elif 'tax' in key:
                                    fields['tax'] = float(value.replace('$', '').replace(',', ''))

    # Items from tables (simplified)
    fields['confidence'] = 0.95  # Placeholder avg
    return ReceiptFields(**fields).model_dump()