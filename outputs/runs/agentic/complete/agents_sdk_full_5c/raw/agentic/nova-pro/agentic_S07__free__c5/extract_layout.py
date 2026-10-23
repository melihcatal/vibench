import boto3

textract = boto3.client('textract')

def extract_layout(document):
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['LAYOUT'])
    layout = response['Blocks']
    return layout