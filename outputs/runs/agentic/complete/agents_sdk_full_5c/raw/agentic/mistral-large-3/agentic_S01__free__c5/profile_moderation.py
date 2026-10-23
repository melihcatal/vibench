import os
from google.cloud import language_v1
from identity_models import RegisterRequest

_moderation_client = None

def get_moderation_client():
    global _moderation_client
    if _moderation_client is None:
        _moderation_client = language_v1.LanguageServiceClient.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    return _moderation_client

def moderate_profile_text(request: RegisterRequest) -> bool:
    client = get_moderation_client()
    document = language_v1.Document(
        content=request.display_name,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment.score
    
    response = client.moderate_text(
        request={
            "document": document,
            "moderation_config": {
                "hate_speech": True,
                "explicit_content": True,
                "harassment": True
            }
        }
    )
    
    for category in response.moderation_categories:
        if category.confidence > 0.8:
            return False
    return True