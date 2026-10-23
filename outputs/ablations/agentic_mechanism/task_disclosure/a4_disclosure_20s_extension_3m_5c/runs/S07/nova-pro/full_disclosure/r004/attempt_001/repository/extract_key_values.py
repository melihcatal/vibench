import boto3

def extract_key_values(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS'])
    key_value_pairs = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_PAIR':
            key = next((child['Text'] for child in block['Relationships'] if child['Type'] == 'CHILD' and child['Id'] == block['Id']), None)
            value = next((child['Text'] for child in block['Relationships'] if child['Type'] == 'VALUE' and child['Id'] == block['Id']), None)
            if key and value:
                key_value_pairs[key] = value
    return key_value_pairs