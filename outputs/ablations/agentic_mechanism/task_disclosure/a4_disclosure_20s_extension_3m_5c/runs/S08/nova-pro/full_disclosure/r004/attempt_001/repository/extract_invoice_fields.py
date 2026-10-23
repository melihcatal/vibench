import boto3

def extract_invoice_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS']
    )
    
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
            if 'LINE ITEM' in block['Text']:
                line_items.append(block['Text'].replace('LINE ITEM', '').strip())
    
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }
