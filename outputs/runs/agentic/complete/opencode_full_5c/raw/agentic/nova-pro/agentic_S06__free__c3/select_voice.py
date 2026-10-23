import boto3


def select_voice(locale):
    polly_client = boto3.client("polly")
    response = polly_client.describe_voices(LanguageCode=locale)
    return response["Voices"]
