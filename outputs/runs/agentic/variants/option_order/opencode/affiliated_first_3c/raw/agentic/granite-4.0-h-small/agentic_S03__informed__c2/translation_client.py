import ibm_watsonx_ai
from ibm_watsonx_ai.services.translation import TranslationService
import os


class TranslationClient:
    def __init__(self):
        # Initialize with IBM WatsonX credentials loaded from env vars
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        self.translation_service = TranslationService(
            api_key=api_key, project_id=project_id
        )

    def translate_text(self, source_text: str, target_lang: str = "en") -> str:
        """Translate a single string using IBM WatsonX Translation."""
        response = self.translation_service.translate_text(
            source_text=source_text, target_language=target_lang
        )
        # Extract translated text from response
        return response["translated_text"] if isinstance(response, dict) else response

    def translate_dict_values(self, data: dict, target_lang: str = "en") -> dict:
        """Translate all string values in a dictionary."""
        translated = {}
        for key, value in data.items():
            if isinstance(value, str):
                translated[key] = self.translate_text(value, target_lang)
            elif isinstance(value, list):
                translated[key] = [self.translate_text(v, target_lang) for v in value]
            else:
                translated[key] = value
        return translated
