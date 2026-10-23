from speech_client import get_language_client
from speech_models import ContentSafetyRequest, ContentSafetyResponse
from google.cloud import language_v1


def script_safety(request: ContentSafetyRequest) -> ContentSafetyResponse:
    client = get_language_client()
    document = language_v1.Document(
        content=request.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)

    is_safe = all(
        category.confidence < 0.7 for category in response.moderation_categories
    )

    categories = {
        category.name: category.confidence
        for category in response.moderation_categories
    }

    return ContentSafetyResponse(is_safe=is_safe, categories=categories)
