import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("comprehend")
    embed_response = client.detect_dominant_language(Text=notes)
    return embed_response["Languages"][0]["LanguageCode"]
