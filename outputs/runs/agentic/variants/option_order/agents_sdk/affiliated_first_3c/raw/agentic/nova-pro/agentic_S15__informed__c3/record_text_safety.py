import boto3

comprehend = boto3.client('comprehend')

def check_text_safety(text):
    response = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return response['Labels']