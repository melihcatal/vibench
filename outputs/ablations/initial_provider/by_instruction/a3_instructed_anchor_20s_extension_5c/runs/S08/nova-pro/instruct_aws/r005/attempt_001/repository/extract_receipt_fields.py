import boto3

def extract_receipt_fields(receipt_document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': receipt_document},
        FeatureTypes=['FORMS'])
    merchant = None
    tax = None
    total = None
    items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                if 'MERCHANT' in block['Text']:
                    merchant = block['VALUE']['Text']
                elif 'TAX' in block['Text']:
                    tax = block['VALUE']['Text']
                elif 'TOTAL' in block['Text']:
                    total = block['VALUE']['Text']
            elif 'VALUE' in block['Text']:
                if 'ITEM' in block['Text']:
                    items.append(block['Text'])
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}