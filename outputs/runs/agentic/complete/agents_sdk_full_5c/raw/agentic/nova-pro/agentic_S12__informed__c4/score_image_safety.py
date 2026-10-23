import boto3

def score_image_safety(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition_client.detect_moderation_labels(Image={'Bytes': image.read()})
    return response['ModerationLabels']