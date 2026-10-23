import os
from google.cloud import language_v1

def moderate_profile_text(profile_text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = language_v1.LanguageServiceClient(api_key=api_key)
    document = language_v1.Document(content=profile_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document)
    sentiment = analysis.document_sentiment
    if sentiment.score < -0.5:
        return 'Profile text is too negative and may be harmful.'
    return 'Profile text is acceptable.'