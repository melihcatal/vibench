import boto3

def select_voice(language_code):
    polly_client = boto3.client('polly')
    response = polly_client.describe_voices(LanguageCode=language_code)
    return response['Voices']