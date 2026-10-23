import boto3

def extract_receipt_fields(receipt_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': receipt_image},
        FeatureTypes=['FORMS', 'TABLES']
    )
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
        elif block['BlockType'] == 'TABLE':
            for cell in block['Relationships'][0]['Ids']:
                cell_block = next(b for b in response['Blocks'] if b['Id'] == cell)
                if cell_block['BlockType'] == 'CELL':
                    items.append(cell_block['Text'])
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}