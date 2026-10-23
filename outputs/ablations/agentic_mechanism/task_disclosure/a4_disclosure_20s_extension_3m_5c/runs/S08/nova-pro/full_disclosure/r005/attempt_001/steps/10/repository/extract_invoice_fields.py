import boto3

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract')

    with open(document_path, 'rb') as document:
        image_bytes = document.read()

    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES', 'FORMS']
    )

    vendor = None
    date = None
    total = None
    line_items = []

    for item in response.get('Blocks', []):
        if item['BlockType'] == 'KEY_VALUE_SET':
            if item['Text'] == 'Vendor':
                vendor = item['Relationships'][0]['Ids'][0]
            elif item['Text'] == 'Date':
                date = item['Relationships'][0]['Ids'][0]
            elif item['Text'] == 'Total':
                total = item['Relationships'][0]['Ids'][0]
        elif item['BlockType'] == 'TABLE':
            for relationship in item['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        if response['Blocks'][child_id]['BlockType'] == 'CELL':
                            line_items.append(response['Blocks'][child_id]['Text'])

    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }
