from.model_client import ModelClient

def stream_generation(text):
    client = ModelClient().get_client()
    result = client.analyze_sentiment(documents=[text])[0]
    yield result