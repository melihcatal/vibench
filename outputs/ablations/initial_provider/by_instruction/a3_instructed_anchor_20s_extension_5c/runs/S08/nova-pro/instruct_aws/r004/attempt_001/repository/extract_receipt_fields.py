import boto3

def extract_receipt_fields(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )
    extracted_fields = {}
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'KEY_VALUE_SET':
            key = item['Text']
            value = item['Relationships'][0]['Ids'][0]
            extracted_fields[key] = value
    return extracted_fields