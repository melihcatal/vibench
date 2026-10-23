import boto3

def initialize_textract_client(region_name='us-west-2'):
    return boto3.client('textract', region_name=region_name)

def extract_text_from_document(document_path, textract_client):
    with open(document_path, 'rb') as document:
        response = textract_client.detect_document_text(Document={'Bytes': document.read()})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text