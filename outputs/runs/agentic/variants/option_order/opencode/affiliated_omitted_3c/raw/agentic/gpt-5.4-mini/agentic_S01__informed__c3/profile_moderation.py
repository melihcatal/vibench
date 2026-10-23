from google.cloud import language_v1


def profile_moderation(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    classification = client.classify_text(request={"document": document})
    categories = [c.name for c in classification.categories]
    return {"allowed": True, "categories": categories}
