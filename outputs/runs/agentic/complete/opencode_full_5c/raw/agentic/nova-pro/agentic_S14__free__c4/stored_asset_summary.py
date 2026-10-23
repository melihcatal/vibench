import boto3


def stored_asset_summary(text):
    client = boto3.client("comprehend")
    response = client.detect_dominant_language(Text=text)
    return response["Languages"][0]["LanguageCode"]
