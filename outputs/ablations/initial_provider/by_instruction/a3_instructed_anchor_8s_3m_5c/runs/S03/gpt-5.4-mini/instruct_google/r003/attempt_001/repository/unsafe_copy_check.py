from google.cloud import language_v1

from translation_models import normalize_text


def unsafe_copy_check(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_text(text), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={"document": document})
    categories = [item.name for item in response.categories]
    return {"provider": "google", "unsafe": any("Sensitive" in item for item in categories), "categories": categories}
