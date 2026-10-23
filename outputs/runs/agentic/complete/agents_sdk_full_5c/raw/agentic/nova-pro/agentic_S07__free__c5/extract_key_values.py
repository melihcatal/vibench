import boto3

textract = boto3.client('textract')

def extract_key_values(document):
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    key_values = response['Blocks']
    return key_values