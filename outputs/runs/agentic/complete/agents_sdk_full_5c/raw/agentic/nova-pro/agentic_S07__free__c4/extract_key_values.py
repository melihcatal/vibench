import boto3

textract_client = boto3.client('textract')

def extract_key_values(document):
    response = textract_client.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    key_values = [(item['KeyDetection']['Text'], item['ValueDetection']['Text']) for item in response['Blocks'] if item['BlockType'] == 'KEY_VALUE_SET']
    return key_values