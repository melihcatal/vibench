import boto3


def embed_caption(text):
    comprehend_client = boto3.client("comprehend", region_name="us-west-2")
    response = comprehend_client.detect_dominant_language(Text=text)
    lang_code = response["Languages"][0]["LanguageCode"]
    embedding_response = comprehend_client.detect_sentiment(
        Text=text, LanguageCode=lang_code
    )
    return embedding_response["Sentiment"]
