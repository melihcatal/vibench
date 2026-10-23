from google.cloud import translate

class TranslationClient:
    def __init__(self, project_id: str):
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{project_id}"

    def translate_text(self, text: str, target_language_code: str, source_language_code: str = None) -> str:
        if source_language_code:
            response = self.client.translate_text(
                parent=self.parent,
                contents=[text],
                mime_type="text/plain",
                source_language_code=source_language_code,
                target_language_code=target_language_code,
            )
        else:
            response = self.client.translate_text(
                parent=self.parent,
                contents=[text],
                mime_type="text/plain",
                target_language_code=target_language_code,
            )

        return response.translations[0].translated_text
