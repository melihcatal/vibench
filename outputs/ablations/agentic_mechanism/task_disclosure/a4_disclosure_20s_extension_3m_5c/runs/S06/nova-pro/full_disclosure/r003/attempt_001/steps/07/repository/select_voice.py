import boto3

def list_voices(locale):
    polly_client = boto3.client('polly')
    voices = polly_client.describe_voices(LanguageCode=locale)
    return voices['Voices']

def select_voice(voice_id):
    polly_client = boto3.client('polly')
    voice = polly_client.describe_voices(VoiceIds=[voice_id])
    return voice['Voices'][0]