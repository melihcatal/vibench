import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES', 'FORMS']
    )
    
    invoice_data = {
        'vendor': None,
        'date': None,
        'total': None,
        'line_items': []
    }
    
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if block['Text'] == 'Vendor':
                invoice_data['vendor'] = block['Relationships'][0]['Ids'][0]
            elif block['Text'] == 'Date':
                invoice_data['date'] = block['Relationships'][0]['Ids'][0]
            elif block['Text'] == 'Total':
                invoice_data['total'] = block['Relationships'][0]['Ids'][0]
        elif block['BlockType'] == 'TABLE':
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        for child_block in response['Blocks']:
                            if child_block['Id'] == child_id:
                                if child_block['BlockType'] == 'CELL':
                                    invoice_data['line_items'].append(child_block['Text'])
    return invoice_data

if __name__ == '__main__':
    document_path = 'sample_invoice.pdf'
    invoice_fields = extract_invoice_fields(document_path)
    print(invoice_fields)