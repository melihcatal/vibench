import boto3

def detect_text(image_path):
    textract = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract.detect_document_text(Document={'Bytes': image.read()})
    return response['Blocks']

if __name__ == '__main__' :
    image_path = 'path_to_your_image.jpg'
    detected_text = detect_text(image_path)
    print(detected_text)