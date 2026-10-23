import os
from google.cloud import language_v1 as language


def check_safety(text: str) -> dict:
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(
        request={"document": document, "encoding_type": language.EncodingType.UTF8}
    )
    return {
        "score": annotations.document_sentiment.score,
        "magnitude": annotations.document_sentiment.magnitude,
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
    }
