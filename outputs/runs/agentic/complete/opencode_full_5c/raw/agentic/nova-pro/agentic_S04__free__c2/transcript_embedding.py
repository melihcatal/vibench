import boto3

comprehend_client = boto3.client("comprehend")


def transcript_embedding(transcript_text):
    response = comprehend_client.detect_sentiment(
        Text=transcript_text, LanguageCode="en"
    )
    return response["Sentiment"]
