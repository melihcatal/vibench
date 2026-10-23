from.model_client import ModelClient

def model_request(text):
    client = ModelClient().get_client()
    return client.analyze_sentiment(documents=[text])[0]