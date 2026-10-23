import os
import json
from typing import Optional, Dict, Any


def get_translation_client():
    """
    Initialize and return a Google Cloud Translation client.

    Returns:
        Google Cloud Translation client instance
    """
    try:
        # Import Google Cloud Translation SDK
        from google.cloud import translate_v2 as translate

        # Check for Google Cloud credentials
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
                "Please set it to the path of your Google Cloud service account key file."
            )

        # Initialize the client
        client = translate.Client()

        return client

    except ImportError:
        raise ImportError(
            "Google Cloud Translation client not installed. "
            "Install with: pip install google-cloud-translate"
        )
    except Exception as e:
        raise Exception(f"Failed to initialize translation client: {str(e)}")


def validate_language_code(lang_code: str) -> bool:
    """
    Validate a language code format.

    Args:
        lang_code: Language code to validate (e.g., "en", "es", "fr-CA")

    Returns:
        True if valid format, False otherwise
    """
    if not isinstance(lang_code, str):
        return False

    # Basic validation: 2-5 characters, letters and hyphens only
    import re

    return bool(re.match(r"^[a-zA-Z]{2}(-[a-zA-Z]{2,3})?$", lang_code))


def get_supported_languages():
    """
    Get list of languages supported by Google Cloud Translation API.

    Returns:
        List of language codes
    """
    client = get_translation_client()
    languages = client.get_languages()
    return [lang["language"] for lang in languages]


def create_translation_request(
    text: str, source_lang: str, target_lang: str, format_type: str = "text"
) -> Dict[str, Any]:
    """
    Create a standardized translation request payload.

    Args:
        text: Text to translate
        source_lang: Source language code
        target_lang: Target language code
        format_type: Format type ("text" or "html")

    Returns:
        Dictionary with request parameters
    """
    return {
        "text": text,
        "source_language": source_lang,
        "target_language": target_lang,
        "format": format_type,
    }
