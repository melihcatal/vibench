import boto3

def extract_key_values(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS'])
    key_values = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            for relationship in block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    child_ids = [child_id['Id'] for child_id in relationship['Ids']]
                    child_blocks = [block for block in response['Blocks'] if block['Id'] in child_ids]
                    key = next((block for block in child_blocks if block['BlockType'] == 'WORD' and block['Text'].lower() == 'key'), None)
                    value = next((block for block in child_blocks if block['BlockType'] == 'WORD' and block['Text'].lower() == 'value'), None)
                    if key and value:
                        key_values[key['Text']] = value['Text']
    return key_values