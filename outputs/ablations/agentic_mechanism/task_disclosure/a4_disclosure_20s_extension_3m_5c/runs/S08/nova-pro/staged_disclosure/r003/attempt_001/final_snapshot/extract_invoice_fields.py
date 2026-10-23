import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['TABLES']
    )
    
    vendor = None
    date = None
    total = None
    line_items = []
    
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'KEY_VALUE_SET':
            if item.get('Text') == 'Vendor':
                vendor = next((child.get('Text') for child in item['Relationships'][0]['Ids']), None)
            elif item.get('Text') == 'Date':
                date = next((child.get('Text') for child in item['Relationships'][0]['Ids']), None)
            elif item.get('Text') == 'Total':
                total = next((child.get('Text') for child in item['Relationships'][0]['Ids']), None)
        elif item['BlockType'] == 'TABLE':
            for relationship in item['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        child_block = next((block for block in response['Blocks'] if block['Id'] == child_id), None)
                        if child_block and child_block['BlockType'] == 'CELL':
                            line_items.append(child_block.get('Text', ''))
    
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }
