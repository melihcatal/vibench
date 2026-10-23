import boto3

def synthesize_ssml(ssml):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(Text=ssml, OutputFormat='mp3', VoiceId='Joanna', TextType='ssml')
    return response['AudioStream'].read()