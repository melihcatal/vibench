import boto3

def score_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(Text=text)
    return response
