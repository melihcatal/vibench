import boto3
import document_client

def extract_text(image_path: str) -> str:
    client = boto3.client('textract')
    image_bytes = document_client.load_image(image_path)
    response = client.detect_document_text(Document={'Bytes': image_bytes})
    full_text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            full_text += block['Text'] + '\\n'
    return full_text.strip()
