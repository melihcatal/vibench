import boto3

def extract_invoice_fields(invoice_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_image},
        FeatureTypes=['FORMS']
    )
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                fields[block['Text']] = ''
            else:
                fields[list(fields.keys())[-1]] = block['Text']
    return fields