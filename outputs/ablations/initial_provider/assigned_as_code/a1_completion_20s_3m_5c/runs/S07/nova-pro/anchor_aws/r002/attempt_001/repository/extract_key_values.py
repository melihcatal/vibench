import boto3


def extract_key_values(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((b for b in response['Blocks'] if b['Id'] == block['Relationships'][0]['Ids'][0] and b['BlockType'] == 'WORD'), None)
            value = next((b for b in response['Blocks'] if b['Id'] == block['Relationships'][0]['Ids'][1] and b['BlockType'] == 'WORD'), None)
            if key and value:
                key_values[key['Text']] = value['Text']
    return key_values