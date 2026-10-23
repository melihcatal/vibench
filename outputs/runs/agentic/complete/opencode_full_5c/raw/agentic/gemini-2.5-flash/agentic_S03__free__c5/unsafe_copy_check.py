from translation_client import get_language_client
from google.cloud.language_v1 import (
    Document,
    DocumentSentiment,
    ClassificationModelOptions,
)


def unsafe_copy_check(text: str) -> str:
    client = get_language_client()

    document = Document(content=text, type_=Document.Type.PLAIN_TEXT)

    # Attempt to classify text for content categories that might indicate unsafety
    # This is a general classification and not a dedicated content moderation API.
    # For robust content moderation, a specialized API would be more appropriate.
    try:
        response = client.classify_text(request={"document": document})
        categories = response.categories

        unsafe_categories = [
            "/Science/Social Science/Politics",
            "/Law & Government/Public Safety",
            "/News/Politics",
        ]
        # This is a very simplistic check. A real unsafe content check would be more sophisticated.
        for category in categories:
            if any(uc in category.name for uc in unsafe_categories):
                return f"Potential unsafe content detected based on category: {category.name} (confidence: {category.confidence:.2f})"

        return "No explicit unsafe content categories detected."
    except Exception as e:
        return (
            f"Could not classify text for unsafe content (API limitation or error): {e}"
        )
