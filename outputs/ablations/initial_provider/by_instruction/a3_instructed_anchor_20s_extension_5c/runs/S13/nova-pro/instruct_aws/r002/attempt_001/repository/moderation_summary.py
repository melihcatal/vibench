import boto3

textract = boto3.client('textract')

def summarize_moderation(document_path):
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['FORMS'])
    return response
