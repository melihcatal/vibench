# alt_text_translate.py
import os
import json
from google.cloud import translate_v2 as translate
from vision_models import get_vision_client


def translate_alt_texts(image_path, target="es"):
    """Translate generated image description(s) to a target language using Google Cloud Translate."""
    client = get_vision_client()
    # Assume description is stored in the summary JSON we created earlier
    summary_path = os.path.splitext(image_path)[0] + "_summary.json"
    with open(summary_path) as f:
        summary = json.load(f)
    description = summary.get("description", "")
    if not description:
        return []
    translate_client = translate.Client()
    result = translate_client.translate(description, target_language=target)
    translated = result["translatedText"]
    # Append translation to summary
    with open(summary_path, "w") as f:
        summary["translated_description"] = translated
        json.dump(summary, f, indent=2)
    return [{"language": target, "text": translated}]
