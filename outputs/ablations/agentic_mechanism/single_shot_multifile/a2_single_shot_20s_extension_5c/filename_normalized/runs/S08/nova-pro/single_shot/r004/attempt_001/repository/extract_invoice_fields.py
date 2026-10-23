import boto3

def extract_invoice_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key = block['Text']
            else:
                fields[key] = block['Text']
    return fields