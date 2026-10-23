from typing import Any, Dict

from translation_client import get_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_dictionary_values(data: Dict[str, Any], source_language: str, target_language: str, *, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    client = get_client()
    result: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            request = TranslationRequest(text=normalize_text(value), source_language=source_language, target_language=target_language, model=model)
            response = client.responses.create(
                model=request.model,
                input=[
                    {"role": "system", "content": "You are a precise translation engine. Return only the translated text."},
                    {"role": "user", "content": f"Translate from {request.source_language} to {request.target_language}: {request.text}"},
                ],
            )
            translated = getattr(response, "output_text", None) or str(response)
            result[key] = TranslationResponse(text=translated).text
        else:
            result[key] = value
    return result
