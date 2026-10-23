import os
import boto3

def check_message_safety(text):
    comprehend = boto3.client('comprehend', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = comprehend.detect_toxic_content(Text=text, LanguageCode='en')
    return response['ToxicContent']