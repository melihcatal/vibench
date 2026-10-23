import boto3

def extract_fields(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(
            Document={'Bytes': document.read()},
            FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((child['Text'] for child in block['Relationships'] if child['Type'] == 'CHILD' and child['Ids'][0] == block['Id']), None)
            value = block['Text']
            fields[key] = value
    return fields