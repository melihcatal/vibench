import boto3

def extract_tables(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(Document={'Bytes': image_bytes}, FeatureTypes=['TABLES'])
    tables = response['Blocks']
    return tables