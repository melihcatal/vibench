"""Provide local configuration and client helper utilities for General Text Translation."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


CONFIG_FILE_PATH = Path("translation_config.json")
ENV_PREFIX = "TRANSLATION_"


def load_translation_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load translation service configuration from file and environment.

    Priority order:
    1. Environment variables with TRANSLATION_ prefix
    2. Configuration file (JSON)
    3. Default values

    Args:
        config_path: Optional path to configuration file.

    Returns:
        Dictionary with merged configuration values.
    """
    config = {}

    if config_path and Path(config_path).exists():
        with open(config_path, "r") as f:
            config.update(json.load(f))
    elif CONFIG_FILE_PATH.exists():
        with open(CONFIG_FILE_PATH, "r") as f:
            config.update(json.load(f))

    env_config = {
        key[len(ENV_PREFIX):].lower(): value
        for key, value in os.environ.items()
        if key.startswith(ENV_PREFIX)
    }
    config.update(env_config)

    defaults = {
        "google_api_key": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""),
        "deepl_api_key": os.environ.get("DEEPL_API_KEY", ""),
        "aws_region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "azure_translator_key": os.environ.get("AZURE_TRANSLATOR_KEY", ""),
        "azure_region": os.environ.get("AZURE_TRANSLATOR_REGION", "global"),
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "default_source_lang": "en",
        "default_target_lang": "es",
        "max_batch_size": 128,
        "request_timeout": 30,
    }

    for key, value in defaults.items():
        if key not in config or not config[key]:
            config[key] = value

    return config


def create_translation_client(provider: str = "google"):
    """Create a translation client for the specified provider.

    Args:
        provider: Translation service provider ('google', 'deepl', 'aws', 'azure').

    Returns:
        Initialized client for the specified provider.

    Raises:
        ValueError: If provider is not supported or credentials are missing.
    """
    config = load_translation_config()

    if provider == "google":
        from google.cloud import translate_v2 as translate
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
        if credentials_path and not Path(credentials_path).exists():
            raise ValueError(f"Google credentials file not found: {credentials_path}")
        return translate.Client()

    elif provider == "deepl":
        import deepl
        api_key = config.get("deepl_api_key")
        if not api_key:
            raise ValueError("DeepL API key not found in configuration")
        return deepl.Translator(api_key)

    elif provider == "aws":
        import boto3
        from botocore.config import Config
        aws_config = Config(
            region_name=config.get("aws_region", "us-east-1"),
            retries={"max_attempts": 3, "mode": "standard"},
        )
        return boto3.client("translate", config=aws_config)

    elif provider == "azure":
        return {
            "endpoint": "https://api.cognitive.microsofttranslator.com",
            "key": config.get("azure_translator_key", ""),
            "region": config.get("azure_region", "global"),
            "api_version": "3.0",
        }

    else:
        raise ValueError(f"Unsupported translation provider: {provider}")


def validate_language_code(code: str) -> bool:
    """Validate a language code against known ISO 639-1 codes.

    Args:
        code: Language code to validate.

    Returns:
        True if the code is valid.
    """
    valid_codes = {
        "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
        "ar", "hi", "bn", "nl", "pl", "tr", "sv", "da", "no", "fi",
        "cs", "el", "he", "th", "vi", "id", "ms", "uk", "ro", "hu",
        "auto",
    }
    return code.lower() in valid_codes


def get_supported_language_pairs() -> Dict[str, list]:
    """Return supported language pairs for common providers.

    Returns:
        Dictionary mapping provider names to lists of supported language codes.
    """
    return {
        "google": [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "bn", "nl", "pl", "tr", "sv", "da", "no", "fi",
            "cs", "el", "he", "th", "vi", "id", "ms", "uk", "ro", "hu",
        ],
        "deepl": [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh",
            "nl", "pl", "sv", "da", "no", "fi", "cs", "el", "hu", "ro",
        ],
        "aws": [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "nl", "pl", "tr", "sv", "da", "no", "fi",
            "cs", "el", "he", "th", "vi", "id", "ms", "uk", "ro", "hu",
        ],
        "azure": [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "bn", "nl", "pl", "tr", "sv", "da", "no", "fi",
            "cs", "el", "he", "th", "vi", "id", "ms", "uk", "ro", "hu",
        ],
    }
