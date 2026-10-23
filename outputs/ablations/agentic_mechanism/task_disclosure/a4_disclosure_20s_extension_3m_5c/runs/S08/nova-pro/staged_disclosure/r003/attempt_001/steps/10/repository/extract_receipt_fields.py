import boto3

def extract_receipt_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    receipt_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = next((b['Text'] for b in response['Blocks'] if b['Id'] == block['Relationships'][0]['Ids'][0]), None)
            if key in ['Merchant', 'Tax', 'Total']:
                receipt_data[key.lower()] = value
        elif block['BlockType'] == 'LINE' and 'Item' in block['Text']:
            receipt_data.setdefault('items', []).append(block['Text'])
    return receipt_data

if __name__ == '__main__':
    with open('sample_receipt.jpg', 'rb') as document:
        receipt_fields = extract_receipt_fields(document.read())
        print(receipt_fields)