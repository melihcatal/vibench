from google.cloud import language_v1

def check_unsafe_copy(payload, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={
        "document": document
    })
    unsafe_categories = []
    for category in response.categories:
        # Example: Check for categories that might indicate unsafe content
        if "Adult" in category.name or "Violent" in category.name or "Hate speech" in category.name:
            unsafe_categories.append(category.name)
    return {
        "text": payload["text"],
        "is_unsafe": bool(unsafe_categories),
        "unsafe_categories": unsafe_categories,
    }
