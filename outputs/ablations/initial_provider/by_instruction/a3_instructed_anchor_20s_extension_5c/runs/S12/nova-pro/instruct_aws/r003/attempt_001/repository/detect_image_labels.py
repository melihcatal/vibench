import boto3

def detect_labels(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'Bytes': image_bytes})
    return response['Labels']