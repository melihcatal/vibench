import os
from typing import Optional, List

from .speech_client import get_client
from .speech_models import SynthesizeRequest, SynthesisResult


def synthesize_text(text: str, voice: str, locale: Optional[str] = None) -> SynthesisResult:
    """Synthesize plain text to an audio byte stream using the hosted Text‑to‑Speech service.

    Uses the Google Cloud Text‑to‑Speech SDK for illustration.
    • Identifies the provider with the `google-cloud-texttospeech` import.
    • Uses the environment variable `GOOGLE_APPLICATION_CREDENTIALS` for auth.
    """
    client = get_client()
    return client.synthesize_speech(
        input_text=text,
        voice_name=voice,
        voice_locale=locale,
    )
