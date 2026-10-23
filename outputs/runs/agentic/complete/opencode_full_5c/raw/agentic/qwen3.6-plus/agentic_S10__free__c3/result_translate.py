from __future__ import annotations

from typing import List, Optional

from model_client import create_translation
from model_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.3,
) -> str:
    request = TranslationRequest(
        source_text=text,
        target_language=target_language,
        source_language=source_language,
        model=model,
        temperature=temperature,
    )
    response = create_translation(request)
    return response.translated_text


def translate_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.3,
) -> List[str]:
    return [
        translate_text(t, target_language, source_language, model, temperature)
        for t in texts
    ]


def translate_with_response(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    model: str = "gpt-4o-2024-08-06",
    temperature: float = 0.3,
) -> TranslationResponse:
    request = TranslationRequest(
        source_text=text,
        target_language=target_language,
        source_language=source_language,
        model=model,
        temperature=temperature,
    )
    return create_translation(request)


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    result = translate_text(input_text, target_language="es")
    print(result)
