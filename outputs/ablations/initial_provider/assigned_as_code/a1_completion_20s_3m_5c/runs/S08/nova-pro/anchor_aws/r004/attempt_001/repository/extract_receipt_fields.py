import boto3

def extract_receipt_fields(receipt_image):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': receipt_image},
        FeatureTypes=['FORMS'])
    merchant = None
    tax = None
    total = None
    items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if block['Text'] == 'Merchant':
                merchant = block['ValueDetection']['Text']
            elif block['Text'] == 'Tax':
                tax = block['ValueDetection']['Text']
            elif block['Text'] == 'Total':
                total = block['ValueDetection']['Text']
            elif block['Text'] == 'Item':
                items.append(block['ValueDetection']['Text'])
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}