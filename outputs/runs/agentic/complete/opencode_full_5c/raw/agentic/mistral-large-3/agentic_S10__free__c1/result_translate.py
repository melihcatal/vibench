from typing import Optional
import os
import httpx
from pydantic import BaseModel, Field


class TranslationConfig(BaseModel):
    api_key: str = Field(..., description="API key for the translation service")
    base_url: str = Field(
        default="https://api.deepl.com/v2/translate",
        description="Base URL for the DeepL translation API",
    )
    target_lang: str = Field(
        default="EN-US", description="Target language for translation"
    )


def load_translation_config() -> TranslationConfig:
    """Load translation configuration from environment variables."""
    return TranslationConfig(
        api_key=os.getenv("DEEPL_API_KEY", ""),
        target_lang=os.getenv("TRANSLATION_TARGET_LANG", "EN-US"),
    )


async def translate_text(text: str, target_lang: Optional[str] = None) -> str:
    """Translate generated model output using DeepL's hosted API."""
    config = load_translation_config()
    target_lang = target_lang if target_lang else config.target_lang

    payload = {
        "auth_key": config.api_key,
        "text": text,
        "target_lang": target_lang,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(config.base_url, data=payload)
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
