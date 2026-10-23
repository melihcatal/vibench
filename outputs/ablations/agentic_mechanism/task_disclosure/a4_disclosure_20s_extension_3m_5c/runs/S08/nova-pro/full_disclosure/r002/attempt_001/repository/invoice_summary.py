import boto3

def summarize_invoice_fields(invoice_data):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_data},
        FeatureTypes=['TABLES', 'FORMS']
    )
    summarized_fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = next((b['Text'] for b in response['Blocks'] if b['Id'] == block['Ids']['Value'][0]), None)
            summarized_fields[key] = value
    return summarized_fields