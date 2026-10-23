import boto3

def extract_fields(document_text):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Text': document_text},
        FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = None
            value = None
            for child_block_id in block['ChildBlocks']:
                child_block = next(b for b in response['Blocks'] if b['Id'] == child_block_id['ChildId'])
                if child_block['BlockType'] == 'WORD':
                    if child_block['Relationships'][0]['Type'] == 'VALUE':
                        value = child_block['Text']
                    else:
                        key = child_block['Text']
            if key and value:
                fields[key] = value
    return fields