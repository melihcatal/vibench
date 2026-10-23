import boto3

def extract_receipt_fields(document_bytes):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document_bytes},
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
        elif block['BlockType'] == 'LINE' and 'Item' in block['Text']:
            items.append(block['Text'])
    return merchant, tax, total, items

if __name__ == '__main__':
    with open('sample_receipt.jpg', 'rb') as document:
        document_bytes = document.read()
        merchant, tax, total, items = extract_receipt_fields(document_bytes)
        print(f'Merchant: {merchant}')
        print(f'Tax: {tax}')
        print(f'Total: {total}')
        print(f'Items: {items}')