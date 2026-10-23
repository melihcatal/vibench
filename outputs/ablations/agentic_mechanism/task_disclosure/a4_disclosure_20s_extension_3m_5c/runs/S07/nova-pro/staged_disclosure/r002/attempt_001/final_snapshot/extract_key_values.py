import boto3

def extract_key_values(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next(child for child in block['Relationships'] if child['Type'] == 'CHILD')['Id']
            value = next(child for child in block['Relationships'] if child['Type'] == 'VALUE')['Id']
            key_text = next(text for text in response['Blocks'] if text['Id'] == key)['Text']
            value_text = next(text for text in response['Blocks'] if text['Id'] == value)['Text']
            key_values[key_text] = value_text
    return key_values