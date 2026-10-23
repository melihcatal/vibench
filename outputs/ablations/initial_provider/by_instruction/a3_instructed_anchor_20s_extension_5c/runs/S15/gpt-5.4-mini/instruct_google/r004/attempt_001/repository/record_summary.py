import os

from google.cloud import language_v1


def summarize_record(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    return {"score": annotations.document_sentiment.score, "magnitude": annotations.document_sentiment.magnitude}
