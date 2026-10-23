import boto3

def extract_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    return response['Blocks']