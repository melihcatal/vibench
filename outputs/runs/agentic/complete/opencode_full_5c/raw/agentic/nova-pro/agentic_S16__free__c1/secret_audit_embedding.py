import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("comprehend")
    embeddings = client.detect_dominant_language(Text=notes)
    return embeddings["Languages"][0]["LanguageCode"]
