import os
from google.cloud import language_v1

# Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = language_v1.LanguageServiceClient()


def profile_moderation(text):
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment.score
    if sentiment < 0:
        return "Moderation required"
    else:
        return "Moderation not required"
