import os
import json
from google.cloud import translate_v2 as translate_client
from local_helpers.observability_client import get_client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("METRICS_PROVIDER", "AZURE_MONITOR")  # default provider
# For translation we use Google Cloud Translation as the concrete service
TRANSLATE_CLIENT = (
    translate_client.Client()
)  # Uses GOOGLE_APPLICATION_CREDENTIALS by default


def translate_note(note_text: str, target_locale: str = "es") -> dict:
    """
    Translate a free-form note (e.g., dashboard description or metric annotation) from the default source
    language (usually en) to the specified target locale using Google Cloud Translation.
    """
    translation = TRANSLATE_CLIENT.translate(note_text, target_language=target_locale)
    return {
        "original": note_text,
        "translated": translation["translatedText"],
        "source": "en",
        "target": target_locale,
    }


def batch_translate_notes(note_dict: dict, target_locale: str = "es") -> dict:
    """
    Translate a dictionary of note IDs to note texts, returning a dict of translated texts.
    """
    return {
        note_id: translate_note(text, target_locale)["translated"]
        for note_id, text in note_dict.items()
    }


def translate_dashboard_notes(
    dashboard_id: str, notes: dict, target_locale: str = "es"
):
    """
    Simulate a provider-specific dashboard note translation step.
    Here we simply call the generic translator; in a real integration you'd push the translated notes
    back to the monitoring service via its API.
    """
    translated = batch_translate_notes(notes, target_locale)
    return {"dashboard_id": dashboard_id, "notes": translated}


if __name__ == "__main__":
    # Simple example (remove when using in production pipelines)
    test_note = "CPU usage is high on the web tier. Investigate scaling options."
    print(json.dumps(translate_note(test_note, "es"), indent=2))
