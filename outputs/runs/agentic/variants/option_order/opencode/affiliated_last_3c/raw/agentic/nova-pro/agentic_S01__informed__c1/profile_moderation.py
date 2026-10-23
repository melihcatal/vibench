import os
from google.cloud import language_v1 as language


def profile_moderation(text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/service-account-file.json"
    )
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(request={"document": document})
    sentiment = analysis.document_sentiment
    if sentiment.score < -0.5:
        return "Moderation required"
    else:
        return "Moderation not required"
