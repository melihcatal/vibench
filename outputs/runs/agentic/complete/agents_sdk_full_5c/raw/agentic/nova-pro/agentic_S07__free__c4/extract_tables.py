import boto3

textract_client = boto3.client('textract')

def extract_tables(document):
    response = textract_client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES'])
    tables = [item for item in response['Blocks'] if item['BlockType'] == 'TABLE']
    return tables