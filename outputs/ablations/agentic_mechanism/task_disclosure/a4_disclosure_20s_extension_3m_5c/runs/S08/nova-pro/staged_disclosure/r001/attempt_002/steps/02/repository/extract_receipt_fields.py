import boto3

def extract_receipt_fields(document_path):
    client = boto3.client('textract')

    with open(document_path, 'rb') as document:
        imageBytes = document.read()

    response = client.analyze_document(
        Document={'Bytes': imageBytes},
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
            if 'Item' in block['Text']:
                items.append(block['Text'].replace('Item', '').strip())

    return {
        'merchant': merchant,
        'tax': tax,
        'total': total,
        'items': items
    }

# Example usage:
# fields = extract_receipt_fields('path_to_receipt_image.jpg')