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
                key_block = next(b for b in response['Blocks'] if b['Id'] == key_block_id)
                key = key_block['Text']
            elif 'VALUE' in block['EntityTypes']:
                value_block_id = block['Id']
                value_block = next(b for b in response['Blocks'] if b['Id'] == value_block_id)
                value = value_block['Text']
                fields[key] = value
    return fields

if __name__ == '__main__':\n    document_text = 'Name: John Doe\nAddress: 123 Main St\nCity: Anytown\nState: CA\nZip: 12345'
    fields = extract_fields(document_text)
    print(fields)