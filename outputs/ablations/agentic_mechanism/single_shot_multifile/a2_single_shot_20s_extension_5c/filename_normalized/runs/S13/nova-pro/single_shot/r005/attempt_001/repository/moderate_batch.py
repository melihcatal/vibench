import os
from google.cloud import language_v1

def moderate_batch(texts):
    client = language_v1.LanguageServiceClient()
    results = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        results.append((response.document_sentiment.score, response.document_sentiment.magnitude))
    return results