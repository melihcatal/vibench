import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("comprehend")
    result = client.detect_dominant_language(Text=notes)
    return result["Languages"][0]["LanguageCode"]
