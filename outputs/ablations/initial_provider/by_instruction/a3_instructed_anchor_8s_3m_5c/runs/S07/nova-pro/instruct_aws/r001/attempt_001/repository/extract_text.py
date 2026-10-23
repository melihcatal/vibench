import boto3

def extract_text(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.detect_document_text(Document={'Bytes': image.read()})
    return response['Blocks']