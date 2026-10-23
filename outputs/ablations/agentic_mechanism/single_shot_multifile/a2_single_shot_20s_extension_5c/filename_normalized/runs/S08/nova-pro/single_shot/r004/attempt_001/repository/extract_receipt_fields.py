import boto3

def extract_receipt_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['TABLES'])
    fields = {'merchant': '', 'tax': '', 'total': '', 'items': []}
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            if'merchant' in block['Text'].lower():
                fields['merchant'] = block['Text']
            elif 'tax' in block['Text'].lower():
                fields['tax'] = block['Text']
            elif 'total' in block['Text'].lower():
                fields['total'] = block['Text']
            elif 'item' in block['Text'].lower():
                fields['items'].append(block['Text'])
    return fields