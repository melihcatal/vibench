import os
from google.cloud import language_v1

def moderation_reason_embedding(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment_score = response.document_sentiment.score
    return sentiment_score

if __name__ == '__main__':
    text = 'Your moderation reason here'
    embedding = moderation_reason_embedding(text)
    print(f'Embedding: {embedding}')
