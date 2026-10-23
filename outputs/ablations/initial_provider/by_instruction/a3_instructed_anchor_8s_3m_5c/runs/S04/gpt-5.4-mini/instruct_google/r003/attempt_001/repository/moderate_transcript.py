from typing import Any, Dict

from google.cloud import language_v1


def moderate_text(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    return {"provider": "google", "moderation": response.moderation_categories, "text": text}
