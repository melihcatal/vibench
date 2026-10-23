import boto3

polly_client = boto3.client('polly')

def synthesize_text(text):
    response = polly_client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return response['AudioStream'].read()