import boto3


def asset_metadata_embedding(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_key_phrases(Text=text, LanguageCode="en")
    print(f"Key phrases: {response}")
    return response
