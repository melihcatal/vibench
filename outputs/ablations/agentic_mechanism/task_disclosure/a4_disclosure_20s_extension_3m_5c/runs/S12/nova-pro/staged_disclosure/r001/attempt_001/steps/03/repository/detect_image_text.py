import boto3

def detect_text(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.detect_document_text(Document={'Bytes': image.read()})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text

if __name__ == '__main__':
    image_path = 'sample_image.jpg'
    detected_text = detect_text(image_path)
    print(detected_text)