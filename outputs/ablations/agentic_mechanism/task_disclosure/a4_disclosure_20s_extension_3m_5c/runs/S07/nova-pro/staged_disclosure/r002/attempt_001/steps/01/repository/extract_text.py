import boto3

def extract_text_from_image(image_path):
    textract = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract.detect_document_text(Document={'Bytes': image.read()})
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    return text

if __name__ == '__main__':
    image_path = 'path_to_your_image.jpg'
    extracted_text = extract_text_from_image(image_path)
    print(extracted_text)