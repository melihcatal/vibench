import boto3

def extract_fields(text):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_text(Text=text)
    return response['TextDetections']