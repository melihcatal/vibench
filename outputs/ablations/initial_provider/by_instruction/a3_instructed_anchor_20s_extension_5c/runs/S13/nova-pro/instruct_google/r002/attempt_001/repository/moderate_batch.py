from google.cloud import language_v1
import os

def moderate_batch(texts):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = language_v1.LanguageServiceClient()
    results = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment = response.document_sentiment
        results.append((text, sentiment.score, sentiment.magnitude))
    return results