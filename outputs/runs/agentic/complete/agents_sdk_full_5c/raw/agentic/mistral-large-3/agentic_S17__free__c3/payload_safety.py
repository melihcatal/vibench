import os
from google.cloud import language_v1
from security_models import DecryptionResponse

def check_payload_safety(response: DecryptionResponse) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=response.plaintext.decode("utf-8"),
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(
        request={"document": document}
    )

    safety_check = {
        "toxic": False,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude
    }

    if response.document_sentiment.score < -0.5:
        safety_check["toxic"] = True

    return safety_check