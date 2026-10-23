import json
from speech_client import get_openai_client
from speech_models import (
    TranslateRequest,
    TranslateResponse,
    normalize_translate_request,
)

OPENAI_TRANSLATE_MODEL = "gpt-4o"


def translate_script(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
    model: str = None,
) -> TranslateResponse:
    client = get_openai_client()

    if model is None:
        model = OPENAI_TRANSLATE_MODEL

    req = TranslateRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        model=model,
    )

    messages = normalize_translate_request(req)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )

    translated_text = response.choices[0].message.content.strip()

    return TranslateResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        model_used=model,
    )


def translate_script_batch(
    texts: list, target_language: str = "en", model: str = None
) -> list:
    results = []
    for text in texts:
        result = translate_script(text, target_language=target_language, model=model)
        results.append(result)
    return results
