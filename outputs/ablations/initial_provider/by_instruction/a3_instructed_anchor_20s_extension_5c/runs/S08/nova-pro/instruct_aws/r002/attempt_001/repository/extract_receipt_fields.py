import boto3

def extract_receipt_fields(receipt_image):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': receipt_image},
        FeatureTypes=['FORMS', 'TABLES']
    )
    extracted_fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = block['Text']
            value = block.get('Relationships', [])[0].get('Text')
            extracted_fields[key] = value
    return extracted_fields