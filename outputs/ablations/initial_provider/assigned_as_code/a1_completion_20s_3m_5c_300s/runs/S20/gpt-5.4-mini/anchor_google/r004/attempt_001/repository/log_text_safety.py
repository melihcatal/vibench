import os

from google.cloud import language_v1


def log_text_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload["text"]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    classification = client.classify_text(request={"document": document})
    categories = [item.name for item in classification.categories]
    unsafe = any("adult" in category.lower() or "violent" in category.lower() for category in categories)
    return {"unsafe": unsafe, "categories": categories}
