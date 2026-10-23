import boto3

def score_safety(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_moderation_labels(Image={'Bytes': image_bytes})
    return response['ModerationLabels']