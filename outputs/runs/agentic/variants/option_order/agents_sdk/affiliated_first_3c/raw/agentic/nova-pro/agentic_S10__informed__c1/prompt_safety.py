import boto3

comprehend = boto3.client('comprehend', region_name='us-east-1')

def check_safety(text):
    response = comprehend.detect_toxic_content(Text=text)
    return response['Toxicity']