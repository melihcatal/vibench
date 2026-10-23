import boto3

def extract_key_values(document):
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    key_values = [(block['KeyDetection']['Text'], block['ValueDetection']['Text']) for block in response['Blocks'] if block['BlockType'] == 'KEY_VALUE_SET']
    return key_values