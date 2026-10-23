import os
from google.cloud import language_v1

def moderate_batch(texts):
    client = language_v1.LanguageServiceClient()
    results = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(document=document)
        results.append(response.document_sentiment.score)
    return results

if __name__ == '__main__':
    sample_texts = ['Text 1 for batch moderation.', 'Text 2 for batch moderation.']
    scores = moderate_batch(sample_texts)
    print(f'Batch sentiment scores: {scores}')
