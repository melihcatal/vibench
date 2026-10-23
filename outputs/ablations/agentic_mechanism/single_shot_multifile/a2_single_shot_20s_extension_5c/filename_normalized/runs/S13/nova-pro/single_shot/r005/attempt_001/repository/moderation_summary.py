import os
from google.cloud import language_v1

def moderation_summary(texts):
    client = language_v1.LanguageServiceClient()
    summaries = []
    for text in texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        summaries.append(response.document_sentiment.score)
    return sum(summaries) / len(summaries) if summaries else 0