from google.cloud import translate

class TranslationClient:
    def __init__(self, project_id: str):
        self.client = translate.TranslationServiceClient()
        self.project_id = project_id

    def translate_text(self, text: str, target_language: str) -> str:
        parent = f"projects/{self.project_id}"
        response = self.client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        return response.translations[0].translated_text
