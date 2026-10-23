import os
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

class MarkupTranslator:
    def __init__(self):
        self.client = translate.Client.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        )

    def translate_markup(
        self, 
        markup: str, 
        target_language: str, 
        source_language: str = None,
        model: str = "nmt"
    ) -> MarkupTranslationResponse:
        soup = BeautifulSoup(markup, "html.parser")
        text_elements = soup.find_all(text=True)

        texts = [text for text in text_elements if text.strip()]
        results = self.client.translate(
            texts,
            target_language=target_language,
            source_language=source_language,
            model=model
        )

        for original, result in zip(text_elements, results):
            if original.strip():
                original.replace_with(result["translatedText"])

        return MarkupTranslationResponse(
            translated_markup=str(soup),
            detected_source_language=results[0].get("detectedSourceLanguage") if results else None,
            model_used=model
        )

def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    translator = MarkupTranslator()
    return translator.translate_markup(
        markup=request.markup,
        target_language=request.target_language,
        source_language=request.source_language
    )