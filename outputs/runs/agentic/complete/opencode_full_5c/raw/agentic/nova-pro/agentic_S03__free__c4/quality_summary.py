import boto3


def summarize_translation_quality(text, translated_text):
    client = boto3.client("comprehend")
    result = client.detect_sentiment(Text=translated_text, LanguageCode="en")
    return result["Sentiment"]
