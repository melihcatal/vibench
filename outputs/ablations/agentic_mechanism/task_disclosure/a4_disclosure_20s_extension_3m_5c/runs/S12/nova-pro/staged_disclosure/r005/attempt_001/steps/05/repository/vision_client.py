import boto3

def create_rekognition_client():
    return boto3.client('rekognition')

def detect_labels(image, max_labels=10, min_confidence=90.0):
    client = create_rekognition_client()
    response = client.detect_labels(
        Image={'Bytes': image},
        MaxLabels=max_labels,
        MinConfidence=min_confidence
    )
    return response['Labels']

def detect_text(image):
    client = create_rekognition_client()
    response = client.detect_text(
        Image={'Bytes': image}
    )
    return response['TextDetections']