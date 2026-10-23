import boto3

client = boto3.client('textract')

def extract_text(document):
    response = client.detect_document_text(Document={'Bytes': document})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text