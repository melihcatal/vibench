import re

from translation_client import get_config, get_openai_client
from translation_models import TranslationResponse


def translate_markup(markup: str, source_language: str, target_language: str) -> TranslationResponse:
    cfg = get_config()
    client = get_openai_client()
    text_only = re.sub(r"<[^>]+>", "", markup)
    response = client.responses.create(model=cfg.openai_model, input=f"Translate while preserving tags from {source_language} to {target_language}: {text_only}")
    return TranslationResponse(translated_text=response.output_text if hasattr(response, "output_text") else markup, provider="openai")
