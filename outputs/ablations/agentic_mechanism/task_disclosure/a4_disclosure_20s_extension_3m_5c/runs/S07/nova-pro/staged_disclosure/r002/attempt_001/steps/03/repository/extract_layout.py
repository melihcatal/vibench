import boto3

def extract_layout(document):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['TABLES', 'FORMS']
    )
    blocks = response['Blocks']
    lines = [block for block in blocks if block['BlockType'] == 'LINE']
    tables = [block for block in blocks if block['BlockType'] == 'TABLE']
    return blocks, lines, tables