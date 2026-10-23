from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client

TRANSLATION_MODEL = "gpt-4.1-mini"


def localize_platform_output(text: str, target_locale: str, client: OpenAI | None = None) -> Dict[str, Any]:
    api_client = client or get_openai_client()
    response = api_client.responses.create(
        model=TRANSLATION_MODEL,
        input=f'Translate the following text to {target_locale}: {text}',
        temperature=0,
        max_output_tokens=1024,
    )
    translated = getattr(response, "output_text", None) or str(response)
    return {"provider": "openai", "model": TRANSLATION_MODEL, "locale": target_locale, "text": translated, "raw": response}
