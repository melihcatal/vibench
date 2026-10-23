import os
from translation_client import get_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_language: str, target_language: str, *, model: str = "gpt-4.1-mini") -> str:
    client = get_client()
    request = TranslationRequest(text=normalize_text(text), source_language=source_language, target_language=target_language, model=model)
    response = client.responses.create(
        model=request.model,
        input=[
            {
                "role": "system",
                "content": "You are a precise translation engine. Return only the translated text.",
            },
            {
                "role": "user",
                "content": f"Translate from {request.source_language} to {request.target_language}: {request.text}",
            },
        ],
    )
    translated = getattr(response, "output_text", None)
    if translated is None:
        translated = str(response)
    return TranslationResponse(text=translated).text
