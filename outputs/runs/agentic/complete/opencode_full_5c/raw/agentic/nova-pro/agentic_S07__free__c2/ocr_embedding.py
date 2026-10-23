import boto3


def embed_text(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_dominant_language(Text=text)
    language_code = response["Languages"][0]["LanguageCode"]
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response["Sentiment"]
