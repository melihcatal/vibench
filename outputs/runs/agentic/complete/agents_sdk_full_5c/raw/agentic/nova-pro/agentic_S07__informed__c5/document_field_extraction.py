import boto3

def extract_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next((c['Text'] for c in block['Relationships'] if c['Type'] == 'CHILD' and c['Ids'][0] == block['Id']), None)
            value = next((c['Text'] for c in block['Relationships'] if c['Type'] == 'VALUE' and c['Ids'][0] == block['Id']), None)
            if key and value:
                fields[key] = value
    return fields