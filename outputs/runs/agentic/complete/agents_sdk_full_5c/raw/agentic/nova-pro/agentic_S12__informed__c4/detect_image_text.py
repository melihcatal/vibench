import boto3

def detect_image_text(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition_client.detect_text(Image={'Bytes': image.read()})
    return response['TextDetections']