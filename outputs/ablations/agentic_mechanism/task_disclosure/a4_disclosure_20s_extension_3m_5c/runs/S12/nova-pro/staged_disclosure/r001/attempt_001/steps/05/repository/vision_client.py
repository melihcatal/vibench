import boto3

def configure_client(region_name='us-west-2'):
    return boto3.client('rekognition', region_name=region_name)

def detect_labels(client, image_bytes):
    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10
    )
    return response['Labels']

def detect_text(client, image_bytes):
    response = client.detect_text(
        Image={'Bytes': image_bytes}
    )
    return response['TextDetections']