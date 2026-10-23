import boto3


def embed_log_message(text):
    client = boto3.client("comprehend")
    response = client.detect_dominant_language(Text=text)
    return response["Languages"][0]["LanguageCode"]
