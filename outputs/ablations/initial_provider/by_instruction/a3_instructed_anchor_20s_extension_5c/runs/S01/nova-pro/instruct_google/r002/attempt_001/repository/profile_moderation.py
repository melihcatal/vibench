import os
from google.cloud import language_v1 as language

def moderate_profile_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    sentiment_score = analysis.document_sentiment.score
    if sentiment_score < -0.5:
        return 'Profile text rejected due to negative sentiment'
    return 'Profile text accepted'