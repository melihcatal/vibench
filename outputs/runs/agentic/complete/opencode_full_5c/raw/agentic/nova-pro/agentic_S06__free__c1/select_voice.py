import boto3


def select_voice(locale):
    polly_client = boto3.client("polly")
    voices = polly_client.describe_voices(LanguageCode=locale)
    return voices["Voices"]
