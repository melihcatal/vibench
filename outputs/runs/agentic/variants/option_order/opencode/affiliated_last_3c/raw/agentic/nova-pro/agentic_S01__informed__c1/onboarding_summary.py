import os
from google.cloud import translate_v2 as translate
from google.cloud import language_v1 as language


def onboarding_summary(text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "path/to/your/service-account-file.json"
    )
    translate_client = translate.Client()
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(request={"document": document})
    sentiment = analysis.document_sentiment
    summary = f"Sentiment: {sentiment.score}, Magnitude: {sentiment.magnitude}"
    return summary
