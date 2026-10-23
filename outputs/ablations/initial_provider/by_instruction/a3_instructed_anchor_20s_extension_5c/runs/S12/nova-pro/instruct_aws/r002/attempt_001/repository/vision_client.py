import boto3

def get_vision_client():
    return boto3.client('rekognition')

def get_text_client():
    return boto3.client('textract')