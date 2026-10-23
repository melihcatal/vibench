import boto3

def extract_tables(document_path):
    client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES'])
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            table = {
                'Id': block['Id'],
                'Relationships': block['Relationships']
            }
            tables.append(table)
    return tables