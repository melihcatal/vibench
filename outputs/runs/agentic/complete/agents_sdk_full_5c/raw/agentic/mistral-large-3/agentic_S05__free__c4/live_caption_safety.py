from google.cloud import language_v1
import os

client = language_v1.LanguageServiceClient.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

def check_unsafe_content(text: str) -> bool:
    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_sentiment(
        request={"document": document, "features": {"extract_document_sentiment": False, "classify_text": True}}
    )
    for category in response.categories:
        if category.confidence > 0.7 and (
            "Violence" in category.name or
            "Toxic" in category.name or
            "Sexual" in category.name
        ):
            return True
    return False