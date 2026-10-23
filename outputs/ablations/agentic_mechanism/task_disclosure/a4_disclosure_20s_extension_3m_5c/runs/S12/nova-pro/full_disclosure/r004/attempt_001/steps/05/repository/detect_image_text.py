import boto3

def detect_text(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        img_bytes = image.read()
    response = client.detect_text(Image={'Bytes': img_bytes})
    return response['TextDetections']