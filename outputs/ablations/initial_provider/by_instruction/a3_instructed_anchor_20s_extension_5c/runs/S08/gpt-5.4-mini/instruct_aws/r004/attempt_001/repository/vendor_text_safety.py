from typing import Any, Dict

from google.cloud import language_v1


def vendor_text_safety(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(request={"document": document})
    return {"provider": "google_cloud_natural_language", "response": response}
