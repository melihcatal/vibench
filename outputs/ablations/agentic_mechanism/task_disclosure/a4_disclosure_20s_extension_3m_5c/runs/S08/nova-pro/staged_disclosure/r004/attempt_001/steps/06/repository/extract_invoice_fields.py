import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': imageBytes},
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

if __name__ == '__main__':\n    document_path = 'path_to_invoice_document'
    fields = extract_invoice_fields(document_path)
    print(fields)