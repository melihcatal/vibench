import boto3

def detect_text(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    return response['TextDetections']