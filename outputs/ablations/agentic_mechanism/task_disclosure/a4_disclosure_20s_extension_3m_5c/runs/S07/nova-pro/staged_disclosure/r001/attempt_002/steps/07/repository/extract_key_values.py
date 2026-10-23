import boto3

def extract_key_values(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((child['Text'] for child in block['Relationships'][0]['Ids'] if child['BlockType'] == 'WORD'), None)
            value = next((child['Text'] for child in block['Relationships'][1]['Ids'] if child['BlockType'] == 'WORD'), None)
            if key and value:
                key_values[key] = value
    return key_values