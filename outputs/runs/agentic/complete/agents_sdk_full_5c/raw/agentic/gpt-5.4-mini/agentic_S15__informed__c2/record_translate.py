from typing import List

from deepL import Translator

from database_models import DocumentOperationResponse

DEEPL_MODEL = "deepl-api"


def translate_text_fields(text_fields: List[str], target_language: str = "en") -> DocumentOperationResponse:
    translator = Translator()
    translated = [translator.translate_text(text, target_lang=target_language).text for text in text_fields]
    return DocumentOperationResponse(ok=True, document={"translated_fields": translated, "provider": DEEPL_MODEL}, message="translated")


if __name__ == "__main__":
    raise SystemExit("This module exposes translate_text_fields() using the DeepL API.")
