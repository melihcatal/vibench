import boto3

def check_script_safety(script):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=script,
        LanguageCode='en'
    )
    return response
