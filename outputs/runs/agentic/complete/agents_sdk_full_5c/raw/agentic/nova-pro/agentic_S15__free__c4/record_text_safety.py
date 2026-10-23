import boto3

def check_text_safety(text):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_moderation_labels(Text=text)
    return response['ModerationLabels']