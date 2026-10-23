import boto3

def extract_text(document):
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    text = ''.join([block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE'])
    return text