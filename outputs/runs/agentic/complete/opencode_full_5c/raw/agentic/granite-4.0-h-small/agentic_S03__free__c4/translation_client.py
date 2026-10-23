# translation_client.py
import os
from typing import Any, Dict

# We will use OpenAI's gpt-4o-mini as the concrete translation provider
OPENAI_MODEL = "gpt-4o-mini"


def get_client() -> Any:
    """Return a configured translation client for the selected provider."""
    # Import OpenAI client lazily to avoid early dependency load
    import openai

    # Load API key from environment for security
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    # Configure translation behavior
    openai.default_model = OPENAI_MODEL

    # Small helper to wrap OpenAI's chat completion for translation
    class TranslationResponse:
        def __init__(self, translated_text: str):
            self.translated_text = translated_text

    def translate(text: str, source_lang: str, target_lang: str) -> TranslationResponse:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a translator. Translate the following text from {source_lang} to {target_lang}:",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.0,
        )
        translated = response["choices"][0]["message"]["content"].strip()
        return TranslationResponse(translated)

    def batch_translate(
        texts: list[str], source_lang: str, target_lang: str
    ) -> list[TranslationResponse]:
        responses = []
        for t in texts:
            resp = translate(t, source_lang, target_lang)
            responses.append(resp)
        return responses

    return type(
        "TranslationClient",
        (),
        {"translate": translate, "batch_translate": batch_translate},
    )()
