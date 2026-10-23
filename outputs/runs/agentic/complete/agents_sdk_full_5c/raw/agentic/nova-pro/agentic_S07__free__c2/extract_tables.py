import boto3

client = boto3.client('textract')

def extract_tables(document):
    response = client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES'])
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            tables.append(block)
    return tables