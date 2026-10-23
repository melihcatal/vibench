import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("comprehend")
    response = client.detect_dominant_language(Text=notes)
    return response["Languages"][0]["LanguageCode"]
