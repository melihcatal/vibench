from google.cloud import language_v1

def check_text_safety(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Currently, the Natural Language API doesn't have a direct 'safety score' for general text like Vision API has for images.
    # However, we can use classify_text or analyze_sentiment/entities to infer potential issues.
    # For direct content moderation, other GCP services or custom solutions would be more appropriate.
    # As a proxy for 'safety', we can check for entities or sentiment that might indicate unsafe content.
    # For this exercise, I will use classify_text as it can identify categories that might be relevant to safety.
    # This is a simplification, and a dedicated content moderation API would be ideal if available.

    response = client.classify_text(document=document)

    safe_categories = []
    unsafe_categories = []

    for category in response.categories:
        # This is a simplistic approach. Real safety checks would be more nuanced.
        # For demonstration, let's assume certain categories are 'safe' and others might need review.
        if "/Science" in category.name or "/News" in category.name or "/Technology" in category.name:
            safe_categories.append(category.name)
        else:
            unsafe_categories.append(category.name)

    # In a real scenario, you'd map categories to safety scores or flags.
    # For now, just indicating if potentially unsafe categories are detected.
    is_text_unsafe = bool(unsafe_categories)

    return {
        "text_content": text_content,
        "is_text_unsafe": is_text_unsafe,
        "detected_categories": [cat.name for cat in response.categories]
    }
