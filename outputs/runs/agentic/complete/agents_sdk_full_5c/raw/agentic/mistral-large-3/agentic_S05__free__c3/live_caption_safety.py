from google.cloud import language_v1
import os

client = language_v1.LanguageServiceClient.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

def check_unsafe_content(text: str) -> bool:
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment
    
    response = client.moderate_text(
        request={"document": document}
    )
    for category in response.moderation_categories:
        if category.confidence > 0.8:
            return True
    return False