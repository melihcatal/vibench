import os
import json
from document_client import StructuredDocClient

def extract_invoice_fields(file_path: str) -> dict:
    """Extract vendor, date, total, and line-item fields from an invoice using AWS Textract.

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
    # Process Textract response to extract required fields
    result = {
        'vendor': None,
        'date': None,
        'total': None,
        'line_items': []
    }
    # Example extraction logic (simplified)
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((item['Text'] for item in block['Entities'] if item['Type'] == 'KEY'), None)
            value = next((item['Text'] for item in block['Entities'] if item['Type'] == 'VALUE'), None)
            if key and value:
                if key.lower() == 'vendor':
                    result['vendor'] = {'text': value, 'confidence': block['Confidence']}
                elif key.lower() == 'date':
                    result['date'] = {'text': value, 'confidence': block['Confidence']}
                elif key.lower() == 'total':
                    result['total'] = {'text': value, 'confidence': block['Confidence']}
        elif block['BlockType'] == 'TABLE':
            # Simple table extraction as line items
            lines = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        cell = next((b for b in response['Blocks'] if b['Id'] == child_id), None)
                        if cell and cell['BlockType'] == 'CELL':
                            lines.append({'text': cell.get('Text'), 'confidence': cell.get('Confidence')})
            result['line_items'].append({'items': lines, 'confidence': block['Confidence']})
    return result
