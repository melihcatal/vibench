from google.cloud import language_v1

from speech_models import normalize_transcript


def is_live_caption_safe(text: str) -> bool:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_transcript(text), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.classify_text(request={"document": document})
    return all(category.name.lower() not in {"adult", "violence", "medical"} for category in response.categories)
