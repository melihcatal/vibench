import boto3

def check_unsafe_copy(text):
    comprehend = boto3.client('comprehend')
    result = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return result['Toxicity']