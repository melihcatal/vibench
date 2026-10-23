import boto3

def extract_fields(document_text):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Text': document_text},
        FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key_block_id = block['Id']
            elif 'VALUE' in block['EntityTypes']:
                value_block_id = block['Id']
                for relationship in block['Relationships']:
                    if relationship['Type'] == 'CHILD' and key_block_id in [child_id for child_id in relationship['Ids']]):
                        key = next(block for block in response['Blocks'] if block['Id'] == key_block_id)['Text']
                        value = block['Text']
                        fields[key] = value
    return fields