import boto3

AWS_REGION = "us-west-2"


def moderation_reason_embedding(text):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    response = comprehend.detect_dominant_language(Text=text)
    language_code = response["Languages"][0]["LanguageCode"]
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response["Sentiment"]
