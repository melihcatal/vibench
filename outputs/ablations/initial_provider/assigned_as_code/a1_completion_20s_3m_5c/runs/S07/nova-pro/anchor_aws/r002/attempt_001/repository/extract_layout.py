import boto3


def extract_layout(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES', 'FORMS'])
    layout = {
        'blocks': [b for b in response['Blocks'] if b['BlockType'] == 'BLOCK'],
        'lines': [b for b in response['Blocks'] if b['BlockType'] == 'LINE'],
        'tables': [b for b in response['Blocks'] if b['BlockType'] == 'TABLE'],
    }
    return layout