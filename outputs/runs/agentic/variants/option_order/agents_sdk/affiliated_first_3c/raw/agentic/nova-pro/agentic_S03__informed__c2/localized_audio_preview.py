import boto3

def generate_audio_preview(text):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())