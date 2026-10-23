from google.cloud import language_v1
from speech_models import SafetyCheckRequest


def check_script_safety(request: SafetyCheckRequest) -> dict:
    """Moderates text for unsafe content."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=request.script_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    safety_ratings = {}
    for category in response.moderation_categories:
        safety_ratings[category.name] = category.confidence

    return safety_ratings
