import boto3


def extract_layout(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['TABLES', 'FORMS'])
    layout = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            layout['tables'] = layout.get('tables', []) + [block]
        elif block['BlockType'] == 'KEY_VALUE_SET':
            layout['key_values'] = layout.get('key_values', []) + [block]
    return layout