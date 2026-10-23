import boto3

def extract_fields(document_text):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Text': document_text},
        FeatureTypes=['FORMS'])
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            key = next(child['Text'] for child in block['Relationships'][0]['Children'] if child['BlockType'] == 'WORD')
            value = next(child['Text'] for child in block['Relationships'][1]['Children'] if child['BlockType'] == 'WORD')
            fields[key] = value
    return fields

# Example usage
document_text = 'Name: John Doe\nAddress: 123 Main St\n'
extracted_fields = extract_fields(document_text)
print(extracted_fields)