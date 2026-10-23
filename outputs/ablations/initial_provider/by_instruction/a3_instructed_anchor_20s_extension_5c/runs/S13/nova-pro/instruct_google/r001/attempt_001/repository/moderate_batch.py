from google.cloud import language_v1
from safety_client import get_language_client

def moderate_batch(texts):
    client = get_language_client()
    results = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment.score
        results.append(sentiment)
    return results
