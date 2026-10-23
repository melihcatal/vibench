import os
import json
from document_client import StructuredDocClient

def extract_receipt_fields(file_path: str) -> dict:
    """Extract merchant, tax, total, and items from a receipt using AWS Textract.

    Returns a dict containing the extracted fields with confidence scores.
    """
    client = StructuredDocClient(
        service_name='textract',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    response = client.analyze_document(
        Document={'bytes': open(file_path, 'rb').read()},
        FeatureTypes=['FORMS']
    )
    result = {
        'merchant': None,
        'tax': None,
        'total': None,
        'items': []
    }
    # Example extraction logic (simplified)
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((item['Text'] for item in block['Entities'] if item['Type'] == 'KEY'), None)
            value = next((item['Text'] for item in block['Entities'] if item['Type'] == 'VALUE'), None)
            if key and value:
                if key.lower() == 'merchant':
                    result['merchant'] = {'text': value, 'confidence': block['Confidence']}
                elif key.lower() == 'tax':
                    result['tax'] = {'text': value, 'confidence': block['Confidence']}
                elif key.lower() == 'total':
                    result['total'] = {'text': value, 'confidence': block['Confidence']}
        elif block['BlockType'] == 'TABLE':
            items = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                        if cell and cell['BlockType'] == 'CELL':
                            items.append({'text': cell.get('Text'), 'confidence': cell.get('Confidence')})
            result['items'].append({'line': items, 'confidence': block['Confidence']})
    return result
