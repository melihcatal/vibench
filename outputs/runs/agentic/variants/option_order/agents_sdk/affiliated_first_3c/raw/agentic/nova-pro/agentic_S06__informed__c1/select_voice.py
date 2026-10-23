import os
import boto3

polly_client = boto3.client('polly', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def select_voice(language_code):
    voices = polly_client.describe_voices(LanguageCode=language_code)['Voices']
    return [voice['Name'] for voice in voices]