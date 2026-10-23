import boto3

def extract_text(document_image):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={'Bytes': document_image}
    )
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text