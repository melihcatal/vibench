import boto3

rekognition = boto3.client('rekognition')

def check_payload_safety(text):
    response = rekognition.detect_moderation_labels(
        Text=text
    )
    return response['ModerationLabels']