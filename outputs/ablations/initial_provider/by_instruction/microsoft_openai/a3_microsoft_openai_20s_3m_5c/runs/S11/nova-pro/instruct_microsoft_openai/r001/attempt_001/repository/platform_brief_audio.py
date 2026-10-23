from.model_client import ModelClient

def generate_briefing(text):
    client = ModelClient().get_client()
    result = client.analyze_sentiment(documents=[text])[0]
    return result.sentiment