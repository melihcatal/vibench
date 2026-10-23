import boto3

textract_client = boto3.client('textract')

def extract_layout(document):
    response = textract_client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES', 'FORMS'])
    layout = [item for item in response['Blocks'] if item['BlockType'] in ['LINE', 'WORD', 'TABLE', 'CELL']]
    return layout