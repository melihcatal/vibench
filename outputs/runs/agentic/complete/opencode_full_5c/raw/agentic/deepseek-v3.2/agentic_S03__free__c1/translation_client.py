import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class TranslationConfig:
    """Configuration for Google Cloud Translation API."""

    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "my-translation-project")
    credentials_path: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    default_source_lang: str = "auto"
    default_target_lang: str = "en"
    use_nmt_model: bool = True


def get_translation_client():
    """Initialize and return a Google Cloud Translation client."""
    try:
        from google.cloud import translate_v2 as translate

        config = TranslationConfig()

        if config.credentials_path and os.path.exists(config.credentials_path):
            client = translate.Client.from_service_account_json(config.credentials_path)
        else:
            client = translate.Client()

        return client
    except ImportError:
        raise ImportError(
            "Google Cloud Translation library not installed. Install with: pip install google-cloud-translate"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize translation client: {e}")


def validate_language_code(lang_code: str) -> bool:
    """Validate if a language code is supported by Google Cloud Translation."""
    supported_languages = [
        "en",
        "es",
        "fr",
        "de",
        "zh",
        "ja",
        "ko",
        "ru",
        "ar",
        "hi",
        "pt",
        "it",
        "nl",
        "pl",
        "sv",
        "da",
        "fi",
        "no",
        "tr",
        "el",
    ]
    return lang_code in supported_languages or lang_code == "auto"


def get_supported_languages():
    """Get list of supported languages from Google Cloud Translation API."""
    try:
        client = get_translation_client()
        languages = client.get_languages()
        return [lang["language"] for lang in languages]
    except Exception:
        return ["en", "es", "fr", "de", "zh", "ja", "ko", "ru"]
