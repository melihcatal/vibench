import boto3


def corpus_safety(texts):
    client = boto3.client("comprehend")
    if isinstance(texts, str):
        texts = [texts]
    return [client.detect_dominant_language(Text=t) for t in texts]
