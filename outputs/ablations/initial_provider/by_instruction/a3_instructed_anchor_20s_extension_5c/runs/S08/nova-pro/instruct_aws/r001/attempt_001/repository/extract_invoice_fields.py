import boto3

def extract_invoice_fields(invoice_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_image},
        FeatureTypes=['FORMS', 'TABLES']
    )
    vendor = None
    date = None
    total = None
    line_items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if block['Text'] == 'Vendor':
                vendor = block['ValueDetection']['Text']
            elif block['Text'] == 'Date':
                date = block['ValueDetection']['Text']
            elif block['Text'] == 'Total':
                total = block['ValueDetection']['Text']
        elif block['BlockType'] == 'TABLE':
            for cell in block['Relationships'][0]['Ids']:
                cell_block = next(b for b in response['Blocks'] if b['Id'] == cell)
                if cell_block['BlockType'] == 'CELL':
                    line_items.append(cell_block['Text'])
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}