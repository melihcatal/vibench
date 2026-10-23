import boto3

def summarize_invoice_fields(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': imageBytes},
        FeatureTypes=['FORMS'])
    
    form_data = {}
    for item in response['Blocks']:
        if item['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in item['Relationships'][0]['Ids']:
                key_block_id = item['Relationships'][0]['Ids'][0]
                key_block = next(block for block in response['Blocks'] if block['Id'] == key_block_id)
                key = key_block['Text']
                value = item['Text']
                form_data[key] = value
    
    return form_data

if __name__ == '__main__'):
    document_path = 'path/to/invoice.pdf'
    summary = summarize_invoice_fields(document_path)
    print(summary)