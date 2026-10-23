import boto3

def extract_text(image_path):
    textract_client = boto3.client('textract')
    
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    
    return text
