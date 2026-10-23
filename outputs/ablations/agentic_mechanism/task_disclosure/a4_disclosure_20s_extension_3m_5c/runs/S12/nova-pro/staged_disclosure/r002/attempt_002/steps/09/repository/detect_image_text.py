import boto3

def detect_text(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.detect_document_text(Document={'Bytes': image.read()})
    return response['Blocks']

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    text_blocks = detect_text(image_path)
    for block in text_blocks:
        if block['BlockType'] == 'LINE':
            print(block['Text'])