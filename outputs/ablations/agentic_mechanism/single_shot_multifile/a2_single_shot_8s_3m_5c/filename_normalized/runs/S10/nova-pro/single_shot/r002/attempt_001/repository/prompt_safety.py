import os
import google.auth
from google.cloud import language_v1

def check_safety(text):
    credentials, project = google.auth.default()
    client = language_v1.LanguageServiceClient(credentials=credentials)
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(request={'document': document})
    return analysis.document_sentiment.score > -0.5