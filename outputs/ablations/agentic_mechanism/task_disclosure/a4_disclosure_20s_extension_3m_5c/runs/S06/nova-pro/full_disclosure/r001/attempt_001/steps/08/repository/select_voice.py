import boto3

def list_voices(locale):
    polly_client = boto3.client('polly')
    response = polly_client.describe_voices(LanguageCode=locale)
    voices = response['Voices']
    for voice in voices:
        print(voice['Name'], voice['Gender'], voice['LanguageName'])

def select_voice(voice_id):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat='mp3',
        Text='Hello, world!'
    )
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())