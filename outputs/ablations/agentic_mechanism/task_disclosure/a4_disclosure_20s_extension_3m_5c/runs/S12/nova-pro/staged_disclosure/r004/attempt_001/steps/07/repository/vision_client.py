import boto3

def create_rekognition_client():
    return boto3.client('rekognition')

def analyze_image(image_bytes):
    client = create_rekognition_client()
    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10
    )
    return response['Labels']