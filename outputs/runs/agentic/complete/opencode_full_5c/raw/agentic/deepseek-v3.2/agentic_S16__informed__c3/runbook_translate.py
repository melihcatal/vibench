import os
from typing import List, Dict, Any
import deepl


def runbook_translate(
    runbook_texts: List[str], target_language: str = "EN"
) -> List[str]:
    """
    Translate secret-rotation runbook notes using DeepL API.

    Args:
        runbook_texts: List of runbook text strings to translate
        target_language: Target language code (e.g., EN, ES, FR, DE, JA)

    Returns:
        List of translated texts
    """
    # DeepL provider-specific configuration
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    # DeepL provider-specific client
    translator = deepl.Translator(auth_key)

    translations = []

    for text in runbook_texts:
        if not text or not text.strip():
            translations.append("")
            continue

        try:
            # Use DeepL SDK for translation
            result = translator.translate_text(text, target_lang=target_language)

            translations.append(result.text)

        except deepl.DeepLException as e:
            error_msg = str(e)
            if "quota exceeded" in error_msg.lower():
                raise RuntimeError(f"DeepL API quota exceeded: {e}") from e
            elif "authorization failed" in error_msg.lower():
                raise PermissionError(f"DeepL authorization failed: {e}") from e
            elif "too many requests" in error_msg.lower():
                raise RuntimeError(f"DeepL rate limit exceeded: {e}") from e
            else:
                raise RuntimeError(f"DeepL translation error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during DeepL translation: {e}") from e

    # Add translation metadata
    if translations:
        # Get usage statistics from DeepL
        try:
            usage = translator.get_usage()
            metadata = {
                "provider": "DeepL",
                "target_language": target_language,
                "character_count": usage.character.count,
                "character_limit": usage.character.limit,
                "character_usage_percent": (
                    usage.character.count / max(usage.character.limit, 1)
                )
                * 100,
                "total_translated": len([t for t in translations if t]),
            }

            result = {"translations": translations, "metadata": metadata}

            return result

        except Exception:
            # If usage check fails, return basic metadata
            result = {
                "translations": translations,
                "metadata": {
                    "provider": "DeepL",
                    "target_language": target_language,
                    "total_translated": len([t for t in translations if t]),
                },
            }
            return result

    return {
        "translations": [],
        "metadata": {"provider": "DeepL", "target_language": target_language},
    }
