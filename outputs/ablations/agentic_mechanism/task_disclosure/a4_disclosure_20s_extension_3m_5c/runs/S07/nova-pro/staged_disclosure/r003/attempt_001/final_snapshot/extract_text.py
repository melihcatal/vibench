import boto3

def extract_text(image_path):
    client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = client.detect_document_text(Document={'Bytes': image.read()})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text