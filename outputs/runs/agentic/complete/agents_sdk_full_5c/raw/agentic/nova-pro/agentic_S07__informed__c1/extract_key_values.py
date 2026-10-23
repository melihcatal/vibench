import boto3

def extract_key_values(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['FORMS'])
    key_values = [(block['KeyDetection']['Text'], block['ValueDetection']['Text']) for block in response['Blocks'] if block['BlockType'] == 'KEY_VALUE_SET']
    return key_values