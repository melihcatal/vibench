import boto3

def summarize_invoice_fields(invoice_data):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': invoice_data},
        FeatureTypes=['FORMS'])
    form_data = response['Blocks']
    summarized_fields = {}
    for block in form_data:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = block['Relationships'][0]['Ids'][0]
            summarized_fields[key] = form_data[value]['Text']
    return summarized_fields