import boto3

def configure_rekognition_client(region_name='us-west-2'):
    return boto3.client('rekognition', region_name=region_name)

def detect_labels(image, max_labels=10, min_confidence=50.0):
    client = configure_rekognition_client()
    response = client.detect_labels(
        Image={'Bytes': image},
        MaxLabels=max_labels,
        MinConfidence=min_confidence
    )
    return response['Labels']