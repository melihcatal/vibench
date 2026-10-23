from google.cloud import language_v1
from typing import Dict, Any

def check_unsafe_copy(text_to_check: str) -> Dict[str, Any]:
    """Checks localized copy for potentially unsafe content using Google Cloud Natural Language API.
    This uses content classification to identify categories that might be considered unsafe.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_to_check,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Use classify_text to get content categories, which can indicate unsafe content.
    # Note: This is not a dedicated moderation API. For stronger moderation, consider Cloud Video Intelligence API
    # or a dedicated content moderation service.
    response = client.classify_text(request={'document': document})

    unsafe_categories = [
        "/Content/Adult",
        "/Content/Violent",
        "/Health/Medical conditions", # Can be sensitive
        "/News/Politics", # Can be sensitive/controversial
        # Add other categories based on your definition of "unsafe"
    ]

    detected_unsafe_categories = []
    for category in response.categories:
        # The API returns categories like '/Science/Astronomy' with confidence
        # We check if any detected category matches our unsafe list.
        for unsafe_cat in unsafe_categories:
            if category.name.startswith(unsafe_cat) and category.confidence > 0.5:
                detected_unsafe_categories.append({"name": category.name, "confidence": category.confidence})

    is_unsafe = len(detected_unsafe_categories) > 0

    return {
        "text": text_to_check,
        "is_potentially_unsafe": is_unsafe,
        "detected_categories": detected_unsafe_categories,
        "recommendation": "Review detected categories for potential policy violations. "
                          "For robust moderation, consider a dedicated content moderation service."
    }

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # safe_text = "This is a benign sentence."
    # unsafe_text = "I hate this terrible world!"
    # print(f"Safe Check: {check_unsafe_copy(safe_text)}")
    # print(f"Unsafe Check: {check_unsafe_copy(unsafe_text)}")
    pass
