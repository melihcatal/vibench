from google.cloud import language_v1 as language

def moderate_transcript_text(text: str) -> dict:
    client = language.LanguageServiceClient()

    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    # Classify text to get content categories and determine if moderation is needed
    response = client.classify_text(request={'document': document})
    
    categories = []
    for category in response.categories:
        categories.append({
            "name": category.name,
            "confidence": category.confidence,
        })

    # For more explicit moderation, you might need to combine with custom models or other services.
    # This example primarily demonstrates content categorization.

    return {
        "text": text,
        "categories": categories,
        "contains_sensitive_content": any(c.name.startswith('/Adult') or c.name.startswith('/Violence') for c in response.categories) # Basic heuristic
    }
