import os
from typing import Optional
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, Formality


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = False,
) -> str:
    client = TranslationClient()

    formality_enum = None
    if formality:
        try:
            formality_enum = Formality(formality)
        except ValueError:
            formality_enum = None

    translated_text = client.translate_text(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality_enum.value if formality_enum else None,
        preserve_formatting=preserve_formatting,
    )

    return translated_text


def translate_text_with_request(request: TranslationRequest) -> TranslationResponse:
    client = TranslationClient()

    translated_text = client.translate_text(
        text=request.text,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
        formality=request.formality.value if request.formality else None,
        preserve_formatting=request.preserve_formatting,
    )

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=None,
        character_count=len(request.text),
    )


if __name__ == "__main__":
    result = translate_text(text="Hello, world!", target_lang="ES", source_lang="EN")
    print(f"Translated text: {result}")
