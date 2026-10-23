import boto3

polly = boto3.client('polly', region_name='us-east-1')

def generate_speech(text):
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open('speech.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())