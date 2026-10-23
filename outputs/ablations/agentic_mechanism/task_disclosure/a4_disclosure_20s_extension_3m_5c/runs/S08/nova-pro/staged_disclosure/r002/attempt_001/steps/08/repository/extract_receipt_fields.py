import boto3

def extract_receipt_fields(receipt_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': receipt_image},
        FeatureTypes=['FORMS'])
    receipt_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'merchant' in block['Text'].lower():
                receipt_data['merchant'] = block['Text']
            elif 'tax' in block['Text'].lower():
                receipt_data['tax'] = block['Text']
            elif 'total' in block['Text'].lower():
                receipt_data['total'] = block['Text']
            elif 'items' in block['Text'].lower():
                receipt_data['items'] = block['Text']
    return receipt_data