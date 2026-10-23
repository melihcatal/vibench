import os
from google.cloud import language_v1

def moderation_summary(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return f'Sentiment score: {response.document_sentiment.score}'
