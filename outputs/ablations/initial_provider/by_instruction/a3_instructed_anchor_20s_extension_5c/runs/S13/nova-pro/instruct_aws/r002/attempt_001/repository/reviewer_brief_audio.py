import boto3

polly = boto3.client('polly')

def generate_reviewer_brief(text):
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    return response
