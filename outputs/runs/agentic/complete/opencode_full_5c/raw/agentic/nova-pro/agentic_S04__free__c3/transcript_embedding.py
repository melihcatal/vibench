import boto3


def transcript_embedding(transcript):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_dominant_language(Text=transcript)
    return response["Languages"][0]["LanguageCode"]
