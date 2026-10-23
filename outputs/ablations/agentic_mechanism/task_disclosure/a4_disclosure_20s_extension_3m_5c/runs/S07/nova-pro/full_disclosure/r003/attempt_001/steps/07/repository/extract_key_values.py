import boto3

def extract_key_values(document_bytes):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document_bytes},
        FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = None
            value = None
            for child_block_id in block['Relationships'][0]['Ids']:
                child_block = next(b for b in response['Blocks'] if b['Id'] == child_block_id)
                if child_block['BlockType'] == 'WORD':
                    if key is None:
                        key = child_block['Text']
                    else:
                        value = child_block['Text']
            if key and value:
                key_values[key] = value
    return key_values