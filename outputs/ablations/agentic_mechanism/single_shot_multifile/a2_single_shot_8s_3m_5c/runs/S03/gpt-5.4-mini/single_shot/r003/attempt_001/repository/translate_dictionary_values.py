import os
from openai import OpenAI
from translation_client import get_openai_client, get_translation_model
from translation_models import DictionaryTranslationRequest, normalize_dictionary_translation_text

_PROVIDER_MODEL = get_translation_model(os.getenv("TRANSLATION_MODEL", "gpt-4o-mini"))


def translate_dictionary_values(data: dict, source_language: str, target_language: str) -> dict:
    client: OpenAI = get_openai_client()
    request = DictionaryTranslationRequest(data=data, source_language=source_language, target_language=target_language)
    response = client.responses.create(model=_PROVIDER_MODEL, input=request.to_prompt())
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = response.output[0].content[0].text
    return normalize_dictionary_translation_text(output_text).translated_data
