from google.cloud import language_v1

def check_unsafe_content(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text to check for categories that might indicate unsafe content
    response = client.classify_text(request={'document': document})

    unsafe_categories = []
    for category in response.categories:
        # The specific categories and confidence thresholds for "unsafe" will depend on requirements.
        # This is an example of checking for certain content types.
        if "/Violence" in category.name or "/Harassment" in category.name or "/Sexual" in category.name:
            unsafe_categories.append({"name": category.name, "confidence": category.confidence})

    if unsafe_categories:
        return {"is_unsafe": True, "categories": unsafe_categories}
    else:
        return {"is_unsafe": False, "categories": []}
