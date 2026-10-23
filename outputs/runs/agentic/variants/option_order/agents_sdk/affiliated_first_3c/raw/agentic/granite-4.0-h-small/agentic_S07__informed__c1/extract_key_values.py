import boto3

# Amazon Textract SDK integration for key-value pair extraction
client = boto3.client('textract')

def extract_key_values(image_bytes):
    '''Extract key-value pairs from a form-like document using Amazon Textract.'''
    response = client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    kv_pairs = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            role = block.get('KeyValueSetRole')
            if role == 'KEY':
                # Store the next VALUE block that follows this KEY
                key_text = block['Text']
                # Find the subsequent VALUE with the same KEY_VALUE_SET ID
                kv_id = block['Id']
                for kv_block in response['Blocks']:
                    if kv_block['BlockType'] == 'KEY_VALUE_SET' and kv_block['Id'] != kv_id:
                        if any(rel['Type'] == 'CHILD' and rel['Ids'] == [kv_id] for rel in kv_block.get('Relationships', [])):
                            value_text = next((v['Text'] for v in response['Blocks'] if v['Id'] == kv_block['Id'] and v['BlockType'] == 'VALUE'), '')
                            kv_pairs[key_text] = value_text
    return kv_pairs
