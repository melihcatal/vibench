from google.cloud import language_v1

def moderate_claim(text_content):
    """
    Moderates a free-text claim using Google Cloud Natural Language API for content classification.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify content to identify categories that might require moderation
    response = client.classify_text(request={"document": document})

    moderation_flags = []
    for category in response.categories:
        # Example: Flag if the content is in a sensitive category.
        # This is a simplified example; actual moderation logic would be more complex.
        if "Sensitive" in category.name or "Violence" in category.name or "Hate speech" in category.name:
            moderation_flags.append(f"Category: {category.name}, Confidence: {category.confidence:.2f}")

    if moderation_flags:
        return {"moderated": True, "flags": moderation_flags}
    else:
        return {"moderated": False, "flags": []}

