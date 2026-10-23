import boto3

def detect_labels(image_path):
    client = boto3.client('rekognition')

    with open(image_path, 'rb') as image:
        image_bytes = image.read()

    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [label['Name'] for label in response['Labels']]
    return labels