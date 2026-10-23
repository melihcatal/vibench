import httpx
from speech_client import (
    OPENAI_CHAT_ENDPOINT,
    get_openai_headers,
    create_http_client,
    build_chat_payload,
    validate_openai_key,
    DEFAULT_CHAT_MODEL,
)
from speech_models import TranslationRequest, TranslationResponse


def translate_script(
    text: str,
    source_lang: str = "auto",
    target_lang: str = "en",
    model: str = DEFAULT_CHAT_MODEL,
) -> TranslationResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    request = TranslationRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        model=model,
    )

    payload = request.to_openai_payload()

    with create_http_client() as client:
        response = client.post(
            OPENAI_CHAT_ENDPOINT,
            headers=get_openai_headers(),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    translated_text = data["choices"][0]["message"]["content"].strip()

    return TranslationResponse(
        translated_text=translated_text,
        source_lang_detected=source_lang,
        target_lang=target_lang,
        model_used=model,
    )


def translate_script_batch(
    texts: list,
    source_lang: str = "auto",
    target_lang: str = "en",
    model: str = DEFAULT_CHAT_MODEL,
) -> list:
    results = []
    for text in texts:
        result = translate_script(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            model=model,
        )
        results.append(result)
    return results


def translate_for_synthesis(
    text: str,
    target_lang: str = "en",
    target_voice: str = "alloy",
) -> TranslationResponse:
    voice_locale_map = {
        "alloy": "en-US",
        "echo": "en-US",
        "fable": "en-GB",
        "onyx": "en-US",
        "nova": "en-US",
        "shimmer": "en-US",
    }

    locale = voice_locale_map.get(target_voice, "en-US")
    lang_code = locale.split("-")[0]

    return translate_script(
        text=text,
        target_lang=lang_code if target_lang == "auto" else target_lang,
    )
