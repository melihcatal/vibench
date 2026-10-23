import boto3

def extract_receipt_fields(receipt_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': receipt_image},
        FeatureTypes=['FORMS'])
    merchant = None
    tax = None
    total = None
    items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'Merchant' in block['Text']:
                merchant = block['Text'].replace('Merchant', '').strip()
            elif 'Tax' in block['Text']:
                tax = block['Text'].replace('Tax', '').strip()
            elif 'Total' in block['Text']:
                total = block['Text'].replace('Total', '').strip()
        elif block['BlockType'] == 'LINE':
            items.append(block['Text'].strip())
    return {
        'merchant': merchant,
        'tax': tax,
        'total': total,
        'items': items
    }