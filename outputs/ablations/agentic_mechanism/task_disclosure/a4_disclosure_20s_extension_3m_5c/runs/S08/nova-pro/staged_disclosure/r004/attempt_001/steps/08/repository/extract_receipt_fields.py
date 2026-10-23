import boto3

def extract_receipt_fields(document_location):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'S3Object':{'Bucket': 'your-bucket-name', 'Name': document_location}},
        FeatureTypes=['TABLES']
    )
    merchant = None
    tax = None
    total = None
    items = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            if 'Merchant' in item['Text']:
                merchant = item['Text'].replace('Merchant:', '').strip()
            elif 'Tax' in item['Text']:
                tax = item['Text'].replace('Tax:', '').strip()
            elif 'Total' in item['Text']:
                total = item['Text'].replace('Total:', '').strip()
        elif item['BlockType'] == 'TABLE':
            for cell in item['Relationships'][0]['Ids']:
                cell_object = next(b for b in response['Blocks'] if b['Id'] == cell)
                if cell_object['BlockType'] == 'CELL':
                    items.append(cell_object['Text'].strip())
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}

# Example usage:
# print(extract_receipt_fields('your-document-key'))