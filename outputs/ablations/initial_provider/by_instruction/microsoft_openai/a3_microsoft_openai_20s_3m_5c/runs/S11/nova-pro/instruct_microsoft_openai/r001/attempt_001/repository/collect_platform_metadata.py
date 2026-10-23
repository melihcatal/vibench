from.model_client import ModelClient

def collect_metadata(text):
    client = ModelClient().get_client()
    result = client.analyze_sentiment(documents=[text])[0]
    return result.sentiment, result.confidence_scores