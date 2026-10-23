from google.cloud import language_v1


def unsafe_copy_check(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload["text"]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    classification = client.classify_text(request={"document": document})
    categories = [item.name for item in classification.categories]
    return {
        "unsafe": any("Sensitive" in category or "Harmful" in category for category in categories),
        "categories": categories,
    }
