import boto3

def extract_invoice_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    
    vendor = None
    date = None
    total = None
    line_items = []
    
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if block['Text'] == 'Vendor':
                vendor = block['Relationships'][0]['Ids'][0]
            elif block['Text'] == 'Date':
                date = block['Relationships'][0]['Ids'][0]
            elif block['Text'] == 'Total':
                total = block['Relationships'][0]['Ids'][0]
            elif block['Text'] == 'Line Items':
                line_items = block['Relationships'][0]['Ids']
    
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }

if __name__ == '__main__':
    with open('invoice.pdf', 'rb') as document:
        fields = extract_invoice_fields(document.read())
        print(fields)