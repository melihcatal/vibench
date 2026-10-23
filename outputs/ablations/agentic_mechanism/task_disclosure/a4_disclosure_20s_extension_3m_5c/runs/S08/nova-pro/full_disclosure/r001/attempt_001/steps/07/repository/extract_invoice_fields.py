import boto3

def extract_invoice_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS']
    )
    vendor = None
    date = None
    total = None
    line_items = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'KEY_VALUE_SET':
            if item['Text'] == 'Vendor':
                vendor = item['Relationships'][0]['Text']
            elif item['Text'] == 'Date':
                date = item['Relationships'][0]['Text']
            elif item['Text'] == 'Total':
                total = item['Relationships'][0]['Text']
        elif item['BlockType'] == 'LINE':
            line_items.append(item['Text'])
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }