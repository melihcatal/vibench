import boto3

def list_voices():
    polly_client = boto3.client('polly')
    voices = polly_client.describe_voices()
    return voices['Voices']

def select_voice(locale):
    polly_client = boto3.client('polly')
    voices = list_voices()
    for voice in voices:
        if voice['LanguageCode'] == locale:
            return voice['Id']
    return None