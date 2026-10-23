"""
Local configuration and client helper utilities for General Text Translation.

Uses DeepL API as the concrete translation provider.
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import Optional

import deepl


def get_deepl_auth_key() -> str:
    """Retrieve the DeepL authentication key from environment."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required. "
            "Set it with your DeepL API key."
        )
    return auth_key


def create_translation_client(
    auth_key: Optional[str] = None,
    *,
    api_url: Optional[str] = None,
    proxy_url: Optional[str] = None,
) -> deepl.Translator:
    """
    Create and return a configured DeepL Translator client.

    Args:
        auth_key: DeepL authentication key. Defaults to DEEPL_AUTH_KEY env var.
        api_url: Optional custom API URL (e.g., for DeepL API Free).
        proxy_url: Optional proxy URL for requests.

    Returns:
        Configured deepl.Translator instance.
    """
    key = auth_key or get_deepl_auth_key()

    kwargs = {}
    if api_url:
        kwargs["server_url"] = api_url
    if proxy_url:
        kwargs["proxy"] = proxy_url

    return deepl.Translator(key, **kwargs)


def get_supported_languages(
    client: Optional[deepl.Translator] = None,
) -> list[dict]:
    """
    Fetch supported source/target languages from DeepL.

    Args:
        client: Optional pre-created DeepL client.

    Returns:
        List of dicts with 'code' and 'name' for each language.
    """
    if client is None:
        client = create_translation_client()

    target_languages = client.get_target_languages()
    return [{"code": lang.code, "name": lang.name} for lang in target_languages]


def validate_language_code(code: str) -> str:
    """
    Normalize and validate a language code for DeepL.

    DeepL uses uppercase codes like 'EN', 'DE', 'FR', etc.
    Some variants like 'EN-US', 'EN-GB', 'PT-BR', 'PT-PT' are supported.

    Args:
        code: Language code string.

    Returns:
        Normalized uppercase language code.

    Raises:
        ValueError: If the code format is invalid.
    """
    if not code:
        raise ValueError("Language code cannot be empty")

    normalized = code.strip().upper()

    valid_prefixes = {
        "AR", "BG", "CS", "DA", "DE", "EL", "EN", "ES", "ET", "FI",
        "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL",
        "PL", "PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH",
    }

    base_code = normalized.split("-")[0]
    if base_code not in valid_prefixes:
        raise ValueError(f"Unsupported language code: {code}")

    return normalized


def get_usage_stats(
    client: Optional[deepl.Translator] = None,
) -> dict:
    """
    Retrieve DeepL API usage statistics.

    Args:
        client: Optional pre-created DeepL client.

    Returns:
        Dict with 'character_count', 'character_limit', etc.
    """
    if client is None:
        client = create_translation_client()

    usage = client.get_usage()
    return {
        "character_count": usage.character.count,
        "character_limit": usage.character.limit,
        "document_count": getattr(usage.document, "count", 0),
        "document_limit": getattr(usage.document, "limit", 0),
        "team_document_count": getattr(usage.team_document, "count", 0),
        "team_document_limit": getattr(usage.team_document, "limit", 0),
    }
