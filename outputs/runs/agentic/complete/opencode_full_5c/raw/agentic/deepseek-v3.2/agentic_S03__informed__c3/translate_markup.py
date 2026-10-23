import os
from typing import Optional, List
import deepl
from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(
    markup_text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    tag_handling: str = "html",
    outline_detection: bool = True,
    non_splitting_tags: Optional[List[str]] = None,
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        markup_text,
        target_lang=target_lang,
        source_lang=source_lang,
        tag_handling=tag_handling,
        outline_detection=outline_detection,
        non_splitting_tags=non_splitting_tags or [],
    )

    return result.text


def translate_markup_with_request(
    request: MarkupTranslationRequest,
) -> MarkupTranslationResponse:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        request.markup_text,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
        tag_handling=request.tag_handling,
        outline_detection=request.outline_detection,
        non_splitting_tags=request.non_splitting_tags or [],
    )

    return MarkupTranslationResponse(
        translated_markup=result.text,
        detected_source_language=result.detected_source_lang,
        character_count=len(request.markup_text),
    )


if __name__ == "__main__":
    html_content = """
    <html>
        <head><title>Welcome</title></head>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a sample paragraph.</p>
            <div>Another section with <strong>bold text</strong>.</div>
        </body>
    </html>
    """

    translated = translate_markup(
        markup_text=html_content, target_lang="ES", source_lang="EN"
    )
    print(f"Translated markup:\n{translated}")
