import boto3

def extract_invoice_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_document(
           Document={'Bytes': document.read()},
           FeatureTypes=['FORMS'])
    invoice_fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['EntityTypes']:
                key = block['Text']
                value = None
                for child_id in block['Relationships'][0]['Ids']:
                    for child_block in response['Blocks']:
                        if child_block['Id'] == child_id and 'VALUE' in child_block['EntityTypes']:
                            value = child_block['Text']
                            break
                    if value:
                        break
                if key.lower() in ['vendor', 'date', 'total']:
                    invoice_fields[key.lower()] = value
    return invoice_fields