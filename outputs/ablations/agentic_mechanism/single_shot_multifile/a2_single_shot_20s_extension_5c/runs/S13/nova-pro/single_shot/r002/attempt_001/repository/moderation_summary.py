import os
from google.cloud import language_v1

def moderation_summary(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(request={'document': document}).document_sentiment
    return {'score': summary.score,'magnitude': summary.magnitude}