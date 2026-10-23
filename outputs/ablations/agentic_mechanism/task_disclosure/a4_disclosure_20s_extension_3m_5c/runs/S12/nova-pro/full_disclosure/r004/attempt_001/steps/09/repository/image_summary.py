import boto3

def summarize_image(image_path):
    client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    response = client.detect_labels(Image={'Bytes': image_bytes})
    labels = [label['Name'] for label in response['Labels']]
    return ', '.join(labels)