import boto3


def embed_translated_segments(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    texts = payload["texts"]
    language_code = payload["language_code"]
    embeddings = []
    for text in texts:
        response = client.detect_dominant_language(Text=text)
        dominant_language = response["Languages"][0]["LanguageCode"]
        if dominant_language == language_code:
            response = client.detect_sentiment(Text=text, LanguageCode=language_code)
            embeddings.append(response["SentimentScore"])
    return {
        "embeddings": embeddings,
    }