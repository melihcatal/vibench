import boto3

def summarize_image(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10
    )
    labels = [label['Name'] for label in response['Labels']]
    return ' '.join(labels)
