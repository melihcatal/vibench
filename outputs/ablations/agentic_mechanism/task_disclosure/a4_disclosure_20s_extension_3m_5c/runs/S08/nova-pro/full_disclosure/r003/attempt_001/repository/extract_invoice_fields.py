import boto3

def extract_invoice_fields(document_path):
    client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    response = client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['FORMS'])
    vendor = None
    date = None
    total = None
    line_items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'VENDOR' in block['Text']:
                vendor = block['Text'].replace('VENDOR', '').strip()
            elif 'DATE' in block['Text']:
                date = block['Text'].replace('DATE', '').strip()
            elif 'TOTAL' in block['Text']:
                total = block['Text'].replace('TOTAL', '').strip()
        elif block['BlockType'] == 'LINE':
            line_items.append(block['Text'].strip())
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }
