import boto3

def list_voices(locale):
    polly_client = boto3.client('polly')
    voices = polly_client.describe_voices(LanguageCode=locale)
    return voices['Voices']

def select_voice(voice_id):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat='mp3',
        Text='Hello, this is a test.'
    )
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Speech synthesized to output.mp3 for voiceId:', voice_id)