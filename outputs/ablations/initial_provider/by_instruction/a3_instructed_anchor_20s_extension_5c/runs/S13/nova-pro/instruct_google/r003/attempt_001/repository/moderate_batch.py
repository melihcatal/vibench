import os
from google.cloud import language_v1

def moderate_batch(texts):
    client = language_v1.LanguageServiceClient()
    results = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment_score = response.document_sentiment.score
        results.append(sentiment_score)
    return results

if __name__ == '__main__':
    texts = ['Text 1', 'Text 2', 'Text 3']
    scores = moderate_batch(texts)
    print(f'Sentiment Scores: {scores}')
