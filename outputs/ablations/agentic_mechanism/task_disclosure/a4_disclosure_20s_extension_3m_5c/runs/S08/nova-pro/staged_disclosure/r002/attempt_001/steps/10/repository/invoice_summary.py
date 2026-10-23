import boto3

def summarize_invoice_fields(invoice_data):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_data},
        FeatureTypes=['FORMS'])
    invoice_summary = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = next((child['Text'] for child in block['Relationships'] if child['Type'] == 'VALUE'), None)
            if value:
                invoice_summary[key] = value
    return invoice_summary