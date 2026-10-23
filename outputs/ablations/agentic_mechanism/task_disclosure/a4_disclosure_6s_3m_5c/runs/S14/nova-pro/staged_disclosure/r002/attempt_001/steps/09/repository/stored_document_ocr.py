import boto3

def run_ocr(document):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'Bytes': document})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text