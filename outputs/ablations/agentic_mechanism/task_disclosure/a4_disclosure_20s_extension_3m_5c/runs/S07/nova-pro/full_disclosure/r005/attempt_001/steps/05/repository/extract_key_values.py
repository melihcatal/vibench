import boto3

def extract_key_values(document_bytes):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=['FORMS'])
    key_value_pairs = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((child['Text'] for child in block['Relationships'][0]['Ids'] if child['BlockType'] == 'WORD'), None)
            value = next((child['Text'] for child in block['Relationships'][1]['Ids'] if child['BlockType'] == 'WORD'), None)
            if key and value:
                key_value_pairs[key] = value
    return key_value_pairs