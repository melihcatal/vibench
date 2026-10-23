import boto3

def detect_text(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    response = client.detect_text(Image={'Bytes': image_bytes})
    text_detections = response['TextDetections']
    return [detection['DetectedText'] for detection in text_detections]
