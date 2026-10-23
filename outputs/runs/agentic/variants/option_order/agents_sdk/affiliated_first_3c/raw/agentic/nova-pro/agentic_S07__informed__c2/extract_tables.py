import boto3

def extract_tables(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['TABLES'])
    return response['Blocks']