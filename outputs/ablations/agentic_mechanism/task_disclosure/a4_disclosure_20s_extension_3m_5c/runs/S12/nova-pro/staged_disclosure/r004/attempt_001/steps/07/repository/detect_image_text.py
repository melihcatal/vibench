import boto3

def detect_text(image_bytes):
    textract = boto3.client('textract')
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text

if __name__ == '__main__':
    with open('sample_image.jpg', 'rb') as image_file:
        image_bytes = image_file.read()
        detected_text = detect_text(image_bytes)
        print(detected_text)