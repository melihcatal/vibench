import requests
from google.cloud import language_v1
from security_models import DecryptionResponse

def check_payload_safety(payload: str) -> bool:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=payload, 
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(
        request={"document": document}
    )

    # Check for unsafe content using sentiment score as a proxy
    return response.document_sentiment.score >= -0.3