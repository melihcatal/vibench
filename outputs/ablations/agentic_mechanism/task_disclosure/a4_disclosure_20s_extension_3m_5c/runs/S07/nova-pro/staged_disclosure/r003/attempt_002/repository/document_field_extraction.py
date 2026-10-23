import boto3

def extract_fields(document_text):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Text': document_text},
        FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = ''
            value = ''
            for child_block_id in block['Relationships'][0]['Ids']:
                child_block = next(b for b in response['Blocks'] if b['Id'] == child_block_id)
                if child_block['BlockType'] == 'WORD':
                    if key == '':
                        key = child_block['Text']
                    else:
                        value = child_block['Text']
            fields[key] = value
    return fields