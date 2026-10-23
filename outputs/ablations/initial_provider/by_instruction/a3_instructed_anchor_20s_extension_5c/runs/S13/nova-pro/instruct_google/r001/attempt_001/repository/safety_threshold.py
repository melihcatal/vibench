from google.cloud import language_v1
from safety_client import get_language_client

def safety_threshold(text, threshold=-0.5):
    client = get_language_client()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment.score
    return sentiment >= threshold
