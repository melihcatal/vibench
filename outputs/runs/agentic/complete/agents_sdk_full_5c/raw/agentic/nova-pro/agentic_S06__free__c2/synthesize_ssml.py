import boto3

polly_client = boto3.client('polly')

def synthesize_ssml(ssml):
    response = polly_client.synthesize_speech(Text=ssml, OutputFormat='mp3', VoiceId='Joanna', TextType='ssml')
    return response['AudioStream'].read()