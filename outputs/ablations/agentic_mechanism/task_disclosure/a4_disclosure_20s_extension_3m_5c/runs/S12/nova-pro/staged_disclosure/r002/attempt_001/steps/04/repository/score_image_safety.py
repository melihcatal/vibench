import boto3

def check_image_safety(image_path):
    rekognition = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        response = rekognition.detect_moderation_labels(
            Image={'Bytes': image.read()}
        )
    return response['ModerationLabels']