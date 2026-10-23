import boto3

def list_voices(locale):
    polly_client = boto3.client('polly')
    voices = polly_client.describe_voices(LanguageCode=locale)
    return voices['Voices']

if __name__ == '__main__':
    locale = 'en-US'  # Example locale
    voices = list_voices(locale)
    for voice in voices:
        print(voice['Name'])