import boto3

client = boto3.client('textract')

def extract_key_values(document):
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key_values[block['Key']] = block['Value']
    return key_values