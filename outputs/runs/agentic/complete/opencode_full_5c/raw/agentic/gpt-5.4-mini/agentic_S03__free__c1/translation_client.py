import os
from typing import Any, Dict, List

from openai import OpenAI

from translation_models import TranslationRequest, TranslationResponse


DEFAULT_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-5.4-mini")


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_text_request(request: TranslationRequest) -> TranslationResponse:
    client = get_client()
    prompt = f"Translate from {request.source_language} to {request.target_language}: {request.normalized_text()}"
    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )
    text = getattr(response, "output_text", "")
    return TranslationResponse(
        translated_text=text,
        provider="openai",
        model=DEFAULT_MODEL,
        metadata={"id": getattr(response, "id", None)},
    )


def translate_many_texts(
    texts: List[str], source_language: str, target_language: str
) -> List[str]:
    return [
        translate_text_request(
            TranslationRequest(item, source_language, target_language)
        ).translated_text
        for item in texts
    ]


def build_markup_prompt(markup: str, source_language: str, target_language: str) -> str:
    return f"Translate the visible text in this markup from {source_language} to {target_language} without changing tags: {markup}"


def build_dictionary_prompt(
    values: Dict[str, Any], source_language: str, target_language: str
) -> str:
    return f"Translate these values from {source_language} to {target_language} and preserve keys: {values}"
