import boto3

def detect_text(image_file):
    textract = boto3.client('textract')
    with open(image_file, 'rb') as image:
        image_bytes = image.read()
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text

if __name__ == '__main__':
    image_file = 'example.jpg'
    detected_text = detect_text(image_file)
    print(detected_text)