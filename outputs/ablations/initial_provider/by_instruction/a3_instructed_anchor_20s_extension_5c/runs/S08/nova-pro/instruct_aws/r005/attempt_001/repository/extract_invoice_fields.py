import boto3

def extract_invoice_fields(invoice_document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_document},
        FeatureTypes=['FORMS'])
    vendor = None
    date = None
    total = None
    line_items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                if 'VENDOR' in block['Text']:
                    vendor = block['VALUE']['Text']
                elif 'DATE' in block['Text']:
                    date = block['VALUE']['Text']
                elif 'TOTAL' in block['Text']:
                    total = block['VALUE']['Text']
            elif 'VALUE' in block['Text']:
                if 'ITEM' in block['Text']:
                    line_items.append(block['Text'])
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}