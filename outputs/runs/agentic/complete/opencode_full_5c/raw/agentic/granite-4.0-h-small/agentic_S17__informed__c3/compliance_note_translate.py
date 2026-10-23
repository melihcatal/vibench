import os
from security_client import KmsClient
from security_models import DecryptRequest, DecryptResponse

# Use Google Gemini for translation (identifiable by the service name)
gemini_client = google_genai.ChatServiceClient()  # type: ignore
TRANSLATOR_MODEL = "gemini-1.5-flash"

# Map language codes to Gemini language identifiers
LANG_MAP = {
    "en": "en-US",
    "es": "es-ES",
    "fr": "fr-FR",
    "de": "de-DE",
}

# Set target language via environment variable (default English)
TARGET_LANG = os.getenv("TRANSLATE_TARGET_LANG", "en")


def translate_compliance_note(note: str, source_lang: str = "en") -> str:
    """Translate a compliance or encryption note to the target language using Gemini.

    Returns the translated text.
    """
    # Prepare the prompt for the translation model
    prompt = gemini_client.ChatMessage(role="user", parts=[note])
    # Call Gemini translation endpoint (simple chat call works for most providers)
    response = gemini_client.chat(model=TRANSLATOR_MODEL, messages=[prompt]).response
    translated = response.candidates[0].content.parts[0].text
    return translated


# Provider identifier visible in code (Google Gemini service)
