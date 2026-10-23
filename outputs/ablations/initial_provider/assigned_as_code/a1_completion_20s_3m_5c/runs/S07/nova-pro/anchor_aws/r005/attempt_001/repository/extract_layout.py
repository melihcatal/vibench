import boto3


def extract_layout(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES', 'FORMS'])
    layout = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            layout.setdefault('lines', []).append(block['Text'])
        elif block['BlockType'] == 'TABLE':
            layout.setdefault('tables', []).append(block)
        elif block['BlockType'] == 'KEY_VALUE_SET':
            layout.setdefault('key_values', []).append((block['Text'], block['Relationships'][0]['Ids'][0]))
    return layout