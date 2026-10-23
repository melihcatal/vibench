import boto3

polly_client = boto3.client('polly')

def select_voice(language_code):
    voices = polly_client.describe_voices(LanguageCode=language_code)['Voices']
    return voices