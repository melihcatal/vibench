import boto3

def select_voice(locale):
    polly = boto3.client('polly')
    voices = polly.describe_voices(LanguageCode=locale)['Voices']
    return voices