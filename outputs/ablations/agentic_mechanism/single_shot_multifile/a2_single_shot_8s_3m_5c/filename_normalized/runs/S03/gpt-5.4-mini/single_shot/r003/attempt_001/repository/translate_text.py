import os
from openai import OpenAI
from translation_client import get_openai_client, get_translation_model
from translation_models import TextTranslationRequest, TextTranslationResponse, normalize_translation_text

_PROVIDER_MODEL = get_translation_model(os.getenv("TRANSLATION_MODEL", "gpt-4o-mini"))


def translate_text(text: str, source_language: str, target_language: str) -> str:
    client: OpenAI = get_openai_client()
    request = TextTranslationRequest(text=text, source_language=source_language, target_language=target_language)
    prompt = request.to_prompt()
    response = client.responses.create(model=_PROVIDER_MODEL, input=prompt)
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = response.output[0].content[0].text
    return normalize_translation_text(output_text).translated_text
