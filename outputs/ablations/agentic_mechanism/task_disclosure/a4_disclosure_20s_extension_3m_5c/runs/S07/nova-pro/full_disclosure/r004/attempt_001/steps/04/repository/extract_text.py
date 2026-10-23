import boto3

def extract_text(document):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'Bytes': document})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text.strip()