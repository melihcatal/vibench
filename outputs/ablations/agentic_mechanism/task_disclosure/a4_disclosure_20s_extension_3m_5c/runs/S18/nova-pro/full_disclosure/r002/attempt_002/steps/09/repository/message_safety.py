import boto3

def check_message_safety(message_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        Text=message_text,
        LanguageCode='en'
    )
    if response['ToxicContent']:
        return False
    else:
        return True