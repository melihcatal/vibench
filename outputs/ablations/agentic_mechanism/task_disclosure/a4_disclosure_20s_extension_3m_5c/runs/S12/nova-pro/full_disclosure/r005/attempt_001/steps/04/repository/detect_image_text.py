import boto3

def detect_text(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'Bytes': image_bytes})
    return response['TextDetections']