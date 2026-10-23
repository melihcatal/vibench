import requests
from translation_client import create_client, build_request_payload
from translation_models import (
    TranslationRequest,
    TranslationResponse,
    NormalizedTranslation,
)

PROVIDER_NAME = "deepl"


async def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """Translate a single text string using the configured provider."""
    client = create_client()
    payload = build_request_payload(text, target_lang, source_lang)
    resp = client.post(
        "https://api.deepl.com/v2/translate",
        json=payload,
        headers={"Authorization": f"DeepL-Auth-Key {os.getenv('DEEPL_API_KEY')}"},
    )
    resp.raise_for_status()
    raw = resp.json()
    # Provider handles HTML tags automatically; just return the first segment
    translated = TranslationResponse(raw).translated[0]
    return translated
