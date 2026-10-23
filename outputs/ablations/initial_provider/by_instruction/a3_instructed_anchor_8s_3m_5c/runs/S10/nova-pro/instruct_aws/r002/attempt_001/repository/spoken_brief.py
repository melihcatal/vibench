import boto3

def generate_spoken_brief(text):
    polly = boto3.client('polly')
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return response['AudioStream'].read()