import boto3


def extract_key_values(payload, config=None):
    config = config or {}
    client = boto3.client("textract", region_name=config.get("region"))
    response = client.analyze_document(Document={'Bytes': payload['document_bytes']}, FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = block['Relationships'][0]['Ids'][0]
            for block in response['Blocks']:
                if block['Id'] == value:
                    key_values[key] = block['Text']
    return key_values