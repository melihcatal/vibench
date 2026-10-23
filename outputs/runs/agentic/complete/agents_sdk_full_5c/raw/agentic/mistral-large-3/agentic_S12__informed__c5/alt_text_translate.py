from google.cloud import translate_v2 as translate
from vision_models import ImageDescriptionResponse

class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.client.translate(text, target_language=target_language)
        return result['translatedText']

def alt_text_translate(description: ImageDescriptionResponse, target_language: str) -> str:
    translator = GoogleTranslateClient()
    return translator.translate_text(description.description, target_language)