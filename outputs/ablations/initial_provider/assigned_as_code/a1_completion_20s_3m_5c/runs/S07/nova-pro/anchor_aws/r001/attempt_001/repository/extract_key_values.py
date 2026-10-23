import boto3


def extract_key_values(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((child['Text'] for child in block['Relationships'][0]['Ids'] if child['BlockType'] == 'WORD'), None)
            value = next((child['Text'] for child in block['Relationships'][1]['Ids'] if child['BlockType'] == 'WORD'), None)
            if key and value:
                key_values[key] = value
    return {'key_values': key_values}