import boto3


def embed_script(script):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_dominant_language(Text=script)
    return response["Languages"][0]["LanguageCode"]
