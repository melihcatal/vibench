from google.cloud import translate_v3

class TranslationClient:
    def __init__(self, project_id: str, location: str = "global"):
        self.client = translate_v3.TranslationServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"

    def translate_text(self, texts: list[str], source_language: str, target_language: str, mime_type: str = "text/plain") -> list[str]:
        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": texts,
                "mime_type": mime_type,
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )
        return [translation.translated_text for translation in response.translations]
