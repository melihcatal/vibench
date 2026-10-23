import os
import deepl
from typing import List, Dict, Any, Optional


def translate_invoice_notes(
    notes: List[str], target_lang: str = "EN-US"
) -> List[Dict[str, Any]]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    results = []
    for note in notes:
        if not note or not note.strip():
            results.append(
                {
                    "original": note,
                    "translated": note,
                    "target_language": target_lang,
                    "success": False,
                    "error": "Empty note",
                }
            )
            continue

        try:
            result = translator.translate_text(note, target_lang=target_lang)

            results.append(
                {
                    "original": note,
                    "translated": result.text,
                    "target_language": target_lang,
                    "detected_source_language": result.detected_source_language,
                    "success": True,
                    "error": None,
                }
            )

        except deepl.DeepLException as e:
            results.append(
                {
                    "original": note,
                    "translated": note,
                    "target_language": target_lang,
                    "success": False,
                    "error": str(e),
                }
            )
        except Exception as e:
            results.append(
                {
                    "original": note,
                    "translated": note,
                    "target_language": target_lang,
                    "success": False,
                    "error": f"Translation error: {str(e)}",
                }
            )

    return results


def translate_vendor_description(
    description: str, target_lang: str = "EN-US"
) -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    if not description or not description.strip():
        return {
            "original": description,
            "translated": description,
            "target_language": target_lang,
            "success": False,
            "error": "Empty description",
        }

    try:
        result = translator.translate_text(description, target_lang=target_lang)

        return {
            "original": description,
            "translated": result.text,
            "target_language": target_lang,
            "detected_source_language": result.detected_source_language,
            "success": True,
            "error": None,
        }

    except deepl.DeepLException as e:
        return {
            "original": description,
            "translated": description,
            "target_language": target_lang,
            "success": False,
            "error": str(e),
        }
    except Exception as e:
        return {
            "original": description,
            "translated": description,
            "target_language": target_lang,
            "success": False,
            "error": f"Translation error: {str(e)}",
        }


def batch_translate_line_items(
    line_items: List[Dict[str, Any]], target_lang: str = "EN-US"
) -> List[Dict[str, Any]]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    translated_items = []
    for item in line_items:
        description = item.get("description", "")
        translated_item = item.copy()

        if description and description.strip():
            try:
                result = translator.translate_text(description, target_lang=target_lang)
                translated_item["translated_description"] = result.text
                translated_item["original_description"] = description
                translated_item["detected_language"] = result.detected_source_language
                translated_item["translation_success"] = True
            except Exception:
                translated_item["translated_description"] = description
                translated_item["original_description"] = description
                translated_item["detected_language"] = "unknown"
                translated_item["translation_success"] = False
        else:
            translated_item["translated_description"] = description
            translated_item["original_description"] = description
            translated_item["detected_language"] = "unknown"
            translated_item["translation_success"] = False

        translated_items.append(translated_item)

    return translated_items


def detect_language(text: str) -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    if not text or not text.strip():
        return {
            "text": text,
            "detected_language": "unknown",
            "confidence": 0.0,
            "success": False,
            "error": "Empty text",
        }

    try:
        usage = translator.get_usage()

        result = translator.translate_text(
            text, target_lang="EN-US", preserve_formatting=True
        )

        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "detected_language": result.detected_source_language,
            "confidence": 1.0,
            "success": True,
            "error": None,
            "character_count": len(text),
            "usage_remaining": usage.character.limit - usage.character.count
            if usage.character.limit
            else None,
        }

    except deepl.DeepLException as e:
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "detected_language": "unknown",
            "confidence": 0.0,
            "success": False,
            "error": str(e),
        }
    except Exception as e:
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "detected_language": "unknown",
            "confidence": 0.0,
            "success": False,
            "error": f"Detection error: {str(e)}",
        }


def get_supported_languages() -> List[Dict[str, str]]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    try:
        source_langs = translator.get_source_languages()
        target_langs = translator.get_target_languages()

        return [
            {"type": "source", "code": lang.code, "name": lang.name}
            for lang in source_langs
        ] + [
            {
                "type": "target",
                "code": lang.code,
                "name": lang.name,
                "supports_formality": lang.supports_formality
                if hasattr(lang, "supports_formality")
                else False,
            }
            for lang in target_langs
        ]

    except Exception as e:
        return [
            {
                "type": "error",
                "code": "error",
                "name": f"Failed to get languages: {str(e)}",
            }
        ]
