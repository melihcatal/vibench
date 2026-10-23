import boto3


def select_voice(config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    response = client.describe_voices(LanguageCode=config.get("language_code", "en-US"))
    voices = response["Voices"]
    return voices