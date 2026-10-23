# dashboard_note_translate.py
# LATER-STEP: Translate metric or dashboard notes for another locale

from observability_client import ObservabilityClient
from observability_models import LocaleTranslationRequest, TranslationResponse


def translate_note(source_text: str, target_locale: str = "fr") -> str:
    """Translate a metric or dashboard note into the requested locale.

    This wrapper calls a generic translation service (provider‑specific) and
    returns only the translated string for easy embedding in UI.

    Args:
        source_text: The original note text.
        target_locale: Destination locale code (e.g., "fr", "es", "zh").

    Returns:
        The translated note as a plain string.
    """
    client = ObservabilityClient()
    payload = LocaleTranslationRequest(
        source_text=source_text, target_locale=target_locale
    )
    resp = client.request("POST", "/translation/notes", json=payload.to_dict())
    # Expected response shape: {"translated": "..."}
    return resp["translated"]


# Example local test
if __name__ == "__main__":
    orig = "High CPU utilization detected on worker nodes."
    french = translate_note(orig, target_locale="fr")
    print("Original:", orig)
    print("French translation:", french)
