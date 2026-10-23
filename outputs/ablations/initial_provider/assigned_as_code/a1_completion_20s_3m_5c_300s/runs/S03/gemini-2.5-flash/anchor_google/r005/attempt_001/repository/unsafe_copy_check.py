import os
from google.cloud import language_v1

def unsafe_copy_check(text: str, config: dict = None) -> dict:
    config = config or {}
    project_id = config.get('project_id') or os.getenv('GOOGLE_CLOUD_PROJECT')

    if not project_id:
        # Although the Natural Language client doesn't strictly require project_id for basic ops,
        # it's good practice for consistency and future features like custom models.
        pass 

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text content to identify potentially unsafe categories
    # This is a basic example; a dedicated content moderation API would be more robust.
    response = client.classify_text(request={'document': document})

    unsafe_categories = [
        "Violence",
        "Hate Speech",
        "Sexual Content",
        "Shocking Content",
        "Harassment & Cyberbullying"
    ] # These are example categories; actual categories depend on the model and service.

    issues = []
    for category in response.categories:
        # The API provides a confidence score, we can set a threshold
        if category.confidence > 0.7 and any(uc.lower() in category.name.lower() for uc in unsafe_categories):
            issues.append({
                "category": category.name,
                "confidence": category.confidence,
                "description": f"Potential unsafe content detected in category: {category.name}"
            })

    return {
        "is_unsafe": len(issues) > 0,
        "issues": issues
    }
