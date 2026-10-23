import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['FORMS'])
    
    vendor = None
    date = None
    total = None
    line_items = []
    
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'VENDOR' in block['Text']:
                vendor = block['Text'].split(':')[1].strip()
            elif 'DATE' in block['Text']:
                date = block['Text'].split(':')[1].strip()
            elif 'TOTAL' in block['Text']:
                total = block['Text'].split(':')[1].strip()
        elif block['BlockType'] == 'LINE':
            if 'ITEM' in block['Text']:
                line_items.append(block['Text'].strip())
    
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }

if __name__ == '__main__':\n    document_path = 'path/to/invoice.pdf'\n    fields = extract_invoice_fields(document_path)\n    print(fields)