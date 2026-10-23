import boto3

def extract_receipt_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    merchant = None
    tax = None
    total = None
    items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'Merchant' in block['Text']:
                merchant = block['Text'].split(': ')[1]
            elif 'Tax' in block['Text']:
                tax = block['Text'].split(': ')[1]
            elif 'Total' in block['Text']:
                total = block['Text'].split(': ')[1]
            elif 'Item' in block['Text']:
                items.append(block['Text'].split(': ')[1])
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}

if __name__ == '__main__':
    with open('receipt.jpg', 'rb') as document:
        receipt_fields = extract_receipt_fields(document.read())
        print(receipt_fields)