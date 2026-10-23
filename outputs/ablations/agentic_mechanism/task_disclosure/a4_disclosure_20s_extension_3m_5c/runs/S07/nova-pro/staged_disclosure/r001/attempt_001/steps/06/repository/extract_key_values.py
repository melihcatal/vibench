import boto3

def extract_key_values(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = None
            value = None
            for child_id in block['ChildIds']:
                child_block = next(b for b in response['Blocks'] if b['Id'] == child_id)
                if child_block['BlockType'] == 'WORD':
                    if key is None:
                        key = child_block['Text']
                    else:
                        value = child_block['Text']
            if key and value:
                key_values[key] = value
    return key_values