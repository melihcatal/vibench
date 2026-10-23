import os
from typing import Dict, List
from google.cloud import translate_v2 as translate


def translate_dashboard_notes(
    notes: Dict[str, str], target_language: str = "es"
) -> Dict[str, str]:
    """Translate metric or dashboard notes for another locale using Google Cloud Translation API."""

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    # Initialize the Translation client
    translate_client = translate.Client()

    # Prepare text for translation
    texts_to_translate = list(notes.values())
    original_keys = list(notes.keys())

    # Perform translation
    try:
        results = translate_client.translate(
            texts_to_translate,
            target_language=target_language,
            source_language="en",  # Assuming English source
        )

        # Map translations back to original keys
        translated_notes = {}
        for i, (key, result) in enumerate(zip(original_keys, results)):
            translated_notes[key] = {
                "original": notes[key],
                "translated": result["translatedText"],
                "detected_source_language": result.get("detectedSourceLanguage", "en"),
                "target_language": target_language,
            }

        return {
            "translations": translated_notes,
            "total_translated": len(translated_notes),
            "target_language": target_language,
            "provider": "Google Cloud Translation API",
        }

    except Exception as e:
        return {
            "error": str(e),
            "total_translated": 0,
            "target_language": target_language,
            "provider": "Google Cloud Translation API",
        }


def translate_metric_descriptions(
    metric_descriptions: List[Dict[str, str]], target_language: str
) -> List[Dict[str, str]]:
    """Translate metric descriptions for dashboard display."""

    translate_client = translate.Client()

    translated_metrics = []

    for metric in metric_descriptions:
        name = metric.get("name", "")
        description = metric.get("description", "")
        unit = metric.get("unit", "")

        # Translate description if it exists
        translated_description = description
        if description:
            try:
                result = translate_client.translate(
                    description, target_language=target_language
                )
                translated_description = result["translatedText"]
            except Exception:
                # Keep original if translation fails
                pass

        translated_metrics.append(
            {
                "name": name,
                "description": translated_description,
                "unit": unit,
                "original_description": description,
                "target_language": target_language,
            }
        )

    return translated_metrics


def get_supported_languages() -> List[Dict[str, str]]:
    """Get list of languages supported by Google Cloud Translation API."""

    translate_client = translate.Client()

    try:
        results = translate_client.get_languages()

        languages = []
        for lang in results:
            languages.append({"language": lang["language"], "name": lang["name"]})

        return {
            "languages": languages,
            "total_languages": len(languages),
            "provider": "Google Cloud Translation API",
        }
    except Exception as e:
        return {"error": str(e), "languages": [], "total_languages": 0}


if __name__ == "__main__":
    dashboard_notes = {
        "cpu_usage": "CPU utilization percentage for the instance",
        "memory_alert": "High memory usage detected - consider scaling",
        "network_traffic": "Inbound and outbound network traffic in bytes",
        "disk_io": "Disk read/write operations per second",
    }

    translation_result = translate_dashboard_notes(dashboard_notes, "fr")
    print(f"Translation results: {translation_result}")

    languages = get_supported_languages()
    print(f"Supported languages count: {languages.get('total_languages', 0)}")
