import boto3

textract = boto3.client('textract')

def extract_tables(document):
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES'])
    tables = response['Blocks']
    return tables