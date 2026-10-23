import boto3

def detect_labels(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'Bytes': image_bytes}, MaxLabels=10)
    return response

def normalize_labels(response):
    labels = [label['Name'] for label in response['Labels']]
    return labels

def detect_text(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'Bytes': image_bytes})
    return response

def normalize_text(response):
    text_detections = [detection['DetectedText'] for detection in response['TextDetections']]
    return text_detections

def detect_moderation_labels(image_bytes):
    client = boto3.client('rekognition')
    response = client.detect_moderation_labels(Image={'Bytes': image_bytes})
    return response

def normalize_moderation_labels(response):
    moderation_labels = [label['Name'] for label in response['ModerationLabels']]
    return moderation_labels