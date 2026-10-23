import os
import google.cloud.texttospeech as tts

# --- Configuration -----------------------------------------------------------
# Credentials can be set via environment variable or explicitly here.
# GOOGLE_APPLICATION_CREDENTIALS=... (preferred)
# ----------------------------------------------------------------------------


def get_client() -> tts.TextToSpeechClient:
    """Provides a lazy-initialized Text‑to‑Speech client.

    The client reads credentials from the standard env var
    GOOGLE_APPLICATION_CREDENTIALS. No hard‑coded keys are used.
    """
    return tts.TextToSpeechClient()


# Example usage (uncomment to test)
# client = get_client()
# voices = client.list_voices(language_code="en-US")
# print([v.name for v in voices.voices])
