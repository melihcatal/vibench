import os
from typing import Dict, List, Optional
from google.cloud import translate_v2 as translate


def translate_dashboard_notes(
    notes: Dict[str, str], target_language: str = "es"
) -> Dict[str, Dict[str, str]]:
    """Translate metric or dashboard notes for another locale."""
    client = translate.Client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    results = {}

    for note_id, text in notes.items():
        if not text or not text.strip():
            results[note_id] = {
                "original": text,
                "translated": text,
                "target_language": target_language,
                "success": True,
                "note": "Empty text, no translation needed",
            }
            continue

        try:
            translation = client.translate(
                text, target_language=target_language, format_="text", model="nmt"
            )

            results[note_id] = {
                "original": text,
                "translated": translation["translatedText"],
                "target_language": target_language,
                "source_language": translation.get("detectedSourceLanguage", "unknown"),
                "success": True,
                "characters": len(text),
                "model": translation.get("model", "nmt"),
            }

        except Exception as e:
            results[note_id] = {
                "original": text,
                "translated": None,
                "target_language": target_language,
                "success": False,
                "error": str(e),
                "note": f"Translation failed: {str(e)}",
            }

    successful = sum(1 for result in results.values() if result["success"])
    total = len(results)

    return {
        "translation_summary": {
            "total_notes": total,
            "successful_translations": successful,
            "failed_translations": total - successful,
            "target_language": target_language,
            "success_rate": (successful / total * 100) if total > 0 else 0,
        },
        "translations": results,
        "supported_languages": get_supported_languages(client),
    }


def get_supported_languages(client) -> List[Dict[str, str]]:
    """Get list of supported languages for translation."""
    try:
        languages = client.get_languages()
        return [{"code": lang["language"], "name": lang["name"]} for lang in languages]
    except Exception as e:
        return [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "ja", "name": "Japanese"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ko", "name": "Korean"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
        ]


def batch_translate_metric_descriptions(
    descriptions: List[Dict[str, str]], target_language: str
) -> Dict[str, Any]:
    """Batch translate metric descriptions."""
    client = translate.Client()

    texts_to_translate = []
    item_ids = []

    for item in descriptions:
        item_id = item.get("id", f"item_{len(texts_to_translate)}")
        text = item.get("description", "")

        if text and text.strip():
            texts_to_translate.append(text)
            item_ids.append(item_id)

    if not texts_to_translate:
        return {"summary": "No texts to translate", "translations": []}

    try:
        translations = client.translate(
            texts_to_translate,
            target_language=target_language,
            format_="text",
            model="nmt",
        )

        results = []
        for i, (item_id, translation) in enumerate(zip(item_ids, translations)):
            original_text = texts_to_translate[i]
            results.append(
                {
                    "id": item_id,
                    "original": original_text,
                    "translated": translation["translatedText"],
                    "source_language": translation.get(
                        "detectedSourceLanguage", "unknown"
                    ),
                    "characters": len(original_text),
                    "success": True,
                }
            )

        return {
            "summary": {
                "total": len(texts_to_translate),
                "successful": len(results),
                "target_language": target_language,
            },
            "translations": results,
        }

    except Exception as e:
        return {
            "summary": {
                "total": len(texts_to_translate),
                "successful": 0,
                "error": str(e),
                "target_language": target_language,
            },
            "translations": [],
        }
