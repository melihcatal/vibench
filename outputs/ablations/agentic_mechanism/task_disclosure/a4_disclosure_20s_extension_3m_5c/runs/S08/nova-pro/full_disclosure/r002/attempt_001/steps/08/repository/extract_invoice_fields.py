import boto3

def extract_invoice_fields(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS']
    )
    extracted_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                key = block['Text'].replace('KEY', '').strip()
                value = block['Text'].replace('VALUE', '').strip()
                extracted_data[key] = value
    return extracted_data