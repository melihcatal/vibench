import boto3

def extract_key_values(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((child for child in block['Relationships'] if child['Type'] == 'CHILD'), None)
            value = next((child for child in block['Relationships'] if child['Type'] == 'VALUE'), None)
            if key and value:
                key_text = next((text['Text'] for text in response['Blocks'] if text['Id'] == key['Ids'][0] and text['BlockType'] == 'WORD'), None)
                value_text = next((text['Text'] for text in response['Blocks'] if text['Id'] == value['Ids'][0] and text['BlockType'] == 'WORD'), None)
                if key_text and value_text:
                    key_values[key_text] = value_text
    return key_values