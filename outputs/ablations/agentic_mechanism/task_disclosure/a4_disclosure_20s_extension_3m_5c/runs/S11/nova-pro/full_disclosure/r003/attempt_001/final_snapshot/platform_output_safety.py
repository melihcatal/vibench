import boto3

def check_unsafe_content(text):
    bedrock = boto3.client('bedrock')
    response = bedrock.detect_toxic_content(Text=text)
    return response
