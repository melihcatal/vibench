import boto3

def detect_text(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.detect_document_text(Document={'Bytes': image.read()})
    text = ' '.join([item['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE' for item in block['Geometry']])
    return text

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    detected_text = detect_text(image_path)
    print(detected_text)