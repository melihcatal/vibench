import boto3

def image_summary(image_path):
    comprehend_client = boto3.client('comprehend')
    with open(image_path, 'rb') as image:
        response = comprehend_client.detect_dominant_language(Text=image.read().decode('utf-8'))
    return response['Languages']