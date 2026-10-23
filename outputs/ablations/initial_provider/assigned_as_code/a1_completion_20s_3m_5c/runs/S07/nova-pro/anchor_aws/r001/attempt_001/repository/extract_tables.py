import boto3


def extract_tables(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES'])
    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            tables.append(block)
    return {'tables': tables}