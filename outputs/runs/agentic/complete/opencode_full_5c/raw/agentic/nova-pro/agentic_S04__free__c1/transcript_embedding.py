import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def embed_transcript(transcript):
    response = comprehend.detect_dominant_language(Text=transcript)
    return response["Languages"][0]["LanguageCode"]
