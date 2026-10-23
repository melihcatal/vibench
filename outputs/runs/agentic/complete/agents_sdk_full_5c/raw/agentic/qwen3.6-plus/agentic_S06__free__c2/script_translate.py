"""
Translate narration scripts before synthesis using Amazon Translate.

This module provides translation of narration scripts between supported
languages using the Amazon Translate service, enabling multi-language
TTS workflows.

Provider: Amazon Translate (translate.us-east-1.amazonaws.com)
Service: AWS Translate v3
"""

from typing import Optional

import boto3
from botocore.config import Config

# Amazon Translate configuration
TRANSLATE_SERVICE_NAME = "translate"
TRANSLATE_DEFAULT_REGION = "us-east-1"

# Language code mappings for Amazon Translate
SUPPORTED_SOURCE_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "hi": "Hindi",
    "ru": "Russian",
}


class TranslateClient:
    """Wrapper around boto3 Amazon Translate client."""

    def __init__(
        self,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.region = region_name or TRANSLATE_DEFAULT_REGION
        
        session_config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
        )
        
        self.client = boto3.client(
            service_name=TRANSLATE_SERVICE_NAME,
            region_name=self.region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=session_config,
        )


def translate_script(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    client: Optional[TranslateClient] = None,
) -> str:
    """
    Translate a narration script using Amazon Translate.
    
    Args:
        text: Source text to translate
        source_language: Source language code (BCP-47 or ISO 639)
        target_language: Target language code (BCP-47 or ISO 639)
        client: Optional pre-configured TranslateClient
        
    Returns:
        Translated text string
    """
    if not client:
        client = TranslateClient()
    
    # Handle BCP-47 codes (e.g., 'en-US' -> 'en')
    src = source_language.split("-")[0]
    tgt = target_language.split("-")[0]
    
    response = client.client.translate_text(
        Text=text,
        SourceLanguageCode=src,
        TargetLanguageCode=tgt,
    )
    
    return response["TranslatedText"]


def translate_batch(
    scripts: list[dict],
    target_language: str,
    client: Optional[TranslateClient] = None,
) -> list[dict]:
    """
    Translate multiple narration scripts using Amazon Translate.
    
    Args:
        scripts: List of dicts with 'text' and optional 'source_language' keys
        target_language: Target language code
        client: Optional pre-configured TranslateClient
        
    Returns:
        List of translated script dicts
    """
    if not client:
        client = TranslateClient()
    
    translated = []
    for script in scripts:
        source_lang = script.get("source_language", "en")
        src = source_lang.split("-")[0]
        tgt = target_language.split("-")[0]
        
        response = client.client.translate_text(
            Text=script["text"],
            SourceLanguageCode=src,
            TargetLanguageCode=tgt,
        )
        
        translated.append({
            **script,
            "translated_text": response["TranslatedText"],
            "target_language": target_language,
            "character_count": response.get("CharacterCount", len(script["text"])),
        })
    
    return translated


def detect_and_translate(
    text: str,
    target_language: str = "es",
    client: Optional[TranslateClient] = None,
) -> dict:
    """
    Auto-detect source language and translate using Amazon Translate.
    
    Uses Amazon Translate's automatic source language detection.
    
    Args:
        text: Text to detect and translate
        target_language: Target language code
        client: Optional pre-configured TranslateClient
        
    Returns:
        Dict with detected source language and translated text
    """
    if not client:
        client = TranslateClient()
    
    tgt = target_language.split("-")[0]
    
    response = client.client.translate_text(
        Text=text,
        SourceLanguageCode="auto",
        TargetLanguageCode=tgt,
    )
    
    return {
        "source_language": response["SourceLanguageCode"],
        "target_language": tgt,
        "translated_text": response["TranslatedText"],
        "character_count": response.get("CharacterCount", len(text)),
    }


if __name__ == "__main__":
    sample = "Welcome to our product demonstration. Today we will explore the key features."
    result = translate_script(sample, source_language="en", target_language="es")
    print(f"Original (en): {sample}")
    print(f"Translated (es): {result}")
