import os
import boto3

def generate_audio_brief(text):
    polly = boto3.client('polly', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open('output.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

if __name__ == '__main__':
    generate_audio_brief('sample text')