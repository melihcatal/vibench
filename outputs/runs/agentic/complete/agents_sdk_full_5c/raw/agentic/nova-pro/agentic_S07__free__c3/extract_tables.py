import boto3

def extract_tables(document):
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES'])
    tables = [block for block in response['Blocks'] if block['BlockType'] == 'TABLE']
    return tables