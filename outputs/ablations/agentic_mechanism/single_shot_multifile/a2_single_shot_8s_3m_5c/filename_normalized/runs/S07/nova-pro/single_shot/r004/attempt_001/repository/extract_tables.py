import boto3

def extract_tables(image_path):
    client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = client.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['TABLES'])
    tables = [block for block in response['Blocks'] if block['BlockType'] == 'TABLE']
    return tables