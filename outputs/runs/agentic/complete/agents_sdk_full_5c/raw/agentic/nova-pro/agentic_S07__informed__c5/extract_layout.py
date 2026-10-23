import boto3

def extract_layout(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['LAYOUT'])
    return response['Blocks']